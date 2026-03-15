# services/db.py - Database Service with local fallback
import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from bson import ObjectId
    from pymongo import MongoClient
except ModuleNotFoundError:
    ObjectId = None
    MongoClient = None


class Database:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("DB_NAME", "browser_automation")
        self.prefer_mongo = os.getenv("USE_MONGO", "").lower() in {"1", "true", "yes"}
        self.local_path = Path(
            os.getenv(
                "LOCAL_DB_PATH",
                Path(__file__).resolve().parent.parent / "data" / "local_db.json",
            )
        )
        self.mode = "local"
        self.client = None
        self.db = None

        self._bootstrap_storage()

    def _bootstrap_storage(self) -> None:
        if MongoClient is None or ObjectId is None:
            print("PyMongo not installed, using local JSON storage instead.")
            self.local_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.local_path.exists():
                self._write_local_data(
                    {"videos": [], "executions": [], "corrections": []}
                )
            return

        if not self.prefer_mongo:
            print("USE_MONGO not enabled, using local JSON storage instead.")
            self.local_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.local_path.exists():
                self._write_local_data(
                    {"videos": [], "executions": [], "corrections": []}
                )
            return

        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=1000)
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            self.videos = self.db.videos
            self.executions = self.db.executions
            self.corrections = self.db.corrections
            self.mode = "mongo"
            self._create_indexes()
            print(f"Database connected in mongo mode: {self.db_name}")
        except Exception as exc:
            print(f"MongoDB unavailable, using local JSON storage instead: {exc}")
            self.mode = "local"
            self.local_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.local_path.exists():
                self._write_local_data(
                    {"videos": [], "executions": [], "corrections": []}
                )

    def _create_indexes(self) -> None:
        if self.mode != "mongo":
            return
        try:
            self.videos.create_index("video_url")
            self.videos.create_index("uploaded_at")
            self.executions.create_index("video_id")
            self.executions.create_index("created_at")
            self.corrections.create_index("execution_id")
            self.corrections.create_index("created_at")
        except Exception as exc:
            print(f"Index creation warning: {exc}")

    def _read_local_data(self) -> Dict[str, List[Dict[str, Any]]]:
        if not self.local_path.exists():
            return {"videos": [], "executions": [], "corrections": []}
        return json.loads(self.local_path.read_text() or "{}")

    def _write_local_data(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        self.local_path.write_text(json.dumps(data, indent=2, default=str))

    @staticmethod
    def _new_id() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def _normalize_id(value: Any) -> str:
        return str(value) if value is not None else ""

    @staticmethod
    def _sort_desc(items: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
        return sorted(items, key=lambda item: item.get(key, ""), reverse=True)

    def insert_video(self, video_doc: Dict[str, Any]) -> str:
        if self.mode == "mongo":
            result = self.videos.insert_one(video_doc)
            return str(result.inserted_id)

        data = self._read_local_data()
        doc = dict(video_doc)
        doc["_id"] = self._new_id()
        data["videos"].append(doc)
        self._write_local_data(data)
        return doc["_id"]

    def get_video_by_id(self, video_id: str) -> Optional[Dict[str, Any]]:
        if self.mode == "mongo":
            video = self.videos.find_one({"_id": ObjectId(video_id)})
            if video:
                video["_id"] = str(video["_id"])
            return video

        for video in self._read_local_data()["videos"]:
            if video.get("_id") == video_id:
                return video
        return None

    def get_all_videos(self) -> List[Dict[str, Any]]:
        if self.mode == "mongo":
            videos = list(self.videos.find().sort("uploaded_at", -1))
            for video in videos:
                video["_id"] = str(video["_id"])
            return videos

        return self._sort_desc(self._read_local_data()["videos"], "uploaded_at")

    def update_video(self, video_id: str, update_doc: Dict[str, Any]) -> bool:
        if self.mode == "mongo":
            result = self.videos.update_one({"_id": ObjectId(video_id)}, {"$set": update_doc})
            return result.modified_count > 0

        data = self._read_local_data()
        for video in data["videos"]:
            if video.get("_id") == video_id:
                video.update(update_doc)
                self._write_local_data(data)
                return True
        return False

    def delete_video(self, video_id: str) -> bool:
        if self.mode == "mongo":
            result = self.videos.delete_one({"_id": ObjectId(video_id)})
            return result.deleted_count > 0

        data = self._read_local_data()
        original_count = len(data["videos"])
        data["videos"] = [video for video in data["videos"] if video.get("_id") != video_id]
        self._write_local_data(data)
        return len(data["videos"]) != original_count

    def find_videos_by_url(self, video_url: str) -> List[Dict[str, Any]]:
        if self.mode == "mongo":
            videos = list(self.videos.find({"video_url": video_url}))
            for video in videos:
                video["_id"] = str(video["_id"])
            return videos

        return [video for video in self._read_local_data()["videos"] if video.get("video_url") == video_url]

    def insert_execution(self, execution_doc: Dict[str, Any]) -> str:
        if self.mode == "mongo":
            doc = dict(execution_doc)
            if doc.get("video_id"):
                try:
                    doc["video_id"] = ObjectId(doc["video_id"])
                except Exception:
                    pass
            result = self.executions.insert_one(doc)
            return str(result.inserted_id)

        data = self._read_local_data()
        doc = dict(execution_doc)
        doc["_id"] = self._new_id()
        doc["video_id"] = self._normalize_id(doc.get("video_id"))
        data["executions"].append(doc)
        self._write_local_data(data)
        return doc["_id"]

    def get_execution_by_id(self, execution_id: str) -> Optional[Dict[str, Any]]:
        if self.mode == "mongo":
            execution = self.executions.find_one({"_id": ObjectId(execution_id)})
            if execution:
                execution["_id"] = str(execution["_id"])
                if execution.get("video_id"):
                    execution["video_id"] = str(execution["video_id"])
            return execution

        for execution in self._read_local_data()["executions"]:
            if execution.get("_id") == execution_id:
                return execution
        return None

    def get_executions_by_video_id(self, video_id: str) -> List[Dict[str, Any]]:
        if self.mode == "mongo":
            query = {"video_id": ObjectId(video_id)}
            executions = list(self.executions.find(query).sort("created_at", -1))
            for execution in executions:
                execution["_id"] = str(execution["_id"])
                execution["video_id"] = str(execution["video_id"])
            return executions

        executions = [
            execution
            for execution in self._read_local_data()["executions"]
            if execution.get("video_id") == video_id
        ]
        return self._sort_desc(executions, "created_at")

    def get_all_executions(self) -> List[Dict[str, Any]]:
        if self.mode == "mongo":
            executions = list(self.executions.find().sort("created_at", -1))
            for execution in executions:
                execution["_id"] = str(execution["_id"])
                if execution.get("video_id"):
                    execution["video_id"] = str(execution["video_id"])
            return executions

        return self._sort_desc(self._read_local_data()["executions"], "created_at")

    def update_execution(self, execution_id: str, update_doc: Dict[str, Any]) -> bool:
        if self.mode == "mongo":
            result = self.executions.update_one(
                {"_id": ObjectId(execution_id)},
                {"$set": update_doc},
            )
            return result.modified_count > 0

        data = self._read_local_data()
        for execution in data["executions"]:
            if execution.get("_id") == execution_id:
                execution.update(update_doc)
                self._write_local_data(data)
                return True
        return False

    def insert_correction(self, correction_doc: Dict[str, Any]) -> str:
        if self.mode == "mongo":
            doc = dict(correction_doc)
            if doc.get("execution_id"):
                try:
                    doc["execution_id"] = ObjectId(doc["execution_id"])
                except Exception:
                    pass
            result = self.corrections.insert_one(doc)
            return str(result.inserted_id)

        data = self._read_local_data()
        doc = dict(correction_doc)
        doc["_id"] = self._new_id()
        doc["execution_id"] = self._normalize_id(doc.get("execution_id"))
        data["corrections"].append(doc)
        self._write_local_data(data)
        return doc["_id"]

    def get_correction_by_id(self, correction_id: str) -> Optional[Dict[str, Any]]:
        if self.mode == "mongo":
            correction = self.corrections.find_one({"_id": ObjectId(correction_id)})
            if correction:
                correction["_id"] = str(correction["_id"])
                if correction.get("execution_id"):
                    correction["execution_id"] = str(correction["execution_id"])
            return correction

        for correction in self._read_local_data()["corrections"]:
            if correction.get("_id") == correction_id:
                return correction
        return None

    def get_corrections_by_execution_id(self, execution_id: str) -> List[Dict[str, Any]]:
        if self.mode == "mongo":
            query = {"execution_id": ObjectId(execution_id)}
            corrections = list(self.corrections.find(query).sort("created_at", -1))
            for correction in corrections:
                correction["_id"] = str(correction["_id"])
                correction["execution_id"] = str(correction["execution_id"])
            return corrections

        corrections = [
            correction
            for correction in self._read_local_data()["corrections"]
            if correction.get("execution_id") == execution_id
        ]
        return self._sort_desc(corrections, "created_at")

    def get_all_corrections(self) -> List[Dict[str, Any]]:
        if self.mode == "mongo":
            corrections = list(self.corrections.find().sort("created_at", -1))
            for correction in corrections:
                correction["_id"] = str(correction["_id"])
                if correction.get("execution_id"):
                    correction["execution_id"] = str(correction["execution_id"])
            return corrections

        return self._sort_desc(self._read_local_data()["corrections"], "created_at")

    def get_execution_stats(self) -> Dict[str, Any]:
        if self.mode == "mongo":
            total_executions = self.executions.count_documents({})
            successful_executions = self.executions.count_documents({"status": "completed"})
            failed_executions = self.executions.count_documents({"status": "failed"})
        else:
            executions = self._read_local_data()["executions"]
            total_executions = len(executions)
            successful_executions = sum(1 for item in executions if item.get("status") == "completed")
            failed_executions = sum(1 for item in executions if item.get("status") == "failed")

        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": (successful_executions / total_executions * 100) if total_executions > 0 else 0,
        }

    def get_recent_activity(self, limit: int = 10) -> Dict[str, Any]:
        if self.mode == "mongo":
            recent_videos = list(self.videos.find().sort("uploaded_at", -1).limit(limit))
            recent_executions = list(self.executions.find().sort("created_at", -1).limit(limit))
            recent_corrections = list(self.corrections.find().sort("created_at", -1).limit(limit))

            for video in recent_videos:
                video["_id"] = str(video["_id"])
            for execution in recent_executions:
                execution["_id"] = str(execution["_id"])
                if execution.get("video_id"):
                    execution["video_id"] = str(execution["video_id"])
            for correction in recent_corrections:
                correction["_id"] = str(correction["_id"])
                if correction.get("execution_id"):
                    correction["execution_id"] = str(correction["execution_id"])

            return {
                "recent_videos": recent_videos,
                "recent_executions": recent_executions,
                "recent_corrections": recent_corrections,
            }

        data = self._read_local_data()
        return {
            "recent_videos": self._sort_desc(data["videos"], "uploaded_at")[:limit],
            "recent_executions": self._sort_desc(data["executions"], "created_at")[:limit],
            "recent_corrections": self._sort_desc(data["corrections"], "created_at")[:limit],
        }

    def cleanup_old_data(self, days: int = 30) -> Dict[str, int]:
        cutoff_iso = (datetime.utcnow() - timedelta(days=days)).isoformat()

        if self.mode == "mongo":
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            executions_deleted = self.executions.delete_many({"created_at": {"$lt": cutoff_date}}).deleted_count
            corrections_deleted = self.corrections.delete_many({"created_at": {"$lt": cutoff_date}}).deleted_count
            return {
                "executions_deleted": executions_deleted,
                "corrections_deleted": corrections_deleted,
            }

        data = self._read_local_data()
        original_executions = len(data["executions"])
        original_corrections = len(data["corrections"])
        data["executions"] = [
            item for item in data["executions"] if item.get("created_at", "") >= cutoff_iso
        ]
        data["corrections"] = [
            item for item in data["corrections"] if item.get("created_at", "") >= cutoff_iso
        ]
        self._write_local_data(data)
        return {
            "executions_deleted": original_executions - len(data["executions"]),
            "corrections_deleted": original_corrections - len(data["corrections"]),
        }

    def close_connection(self) -> None:
        if self.client:
            try:
                self.client.close()
            except Exception as exc:
                print(f"Error closing database connection: {exc}")

    def health_check(self) -> Dict[str, Any]:
        if self.mode == "mongo":
            try:
                self.client.admin.command("ping")
                return {
                    "status": "healthy",
                    "connected": True,
                    "mode": "mongo",
                    "database": self.db_name,
                    "collections": {
                        "videos": self.videos.count_documents({}),
                        "executions": self.executions.count_documents({}),
                        "corrections": self.corrections.count_documents({}),
                    },
                }
            except Exception as exc:
                return {
                    "status": "unhealthy",
                    "connected": False,
                    "mode": "mongo",
                    "error": str(exc),
                }

        data = self._read_local_data()
        return {
            "status": "healthy",
            "connected": True,
            "mode": "local",
            "database": str(self.local_path),
            "collections": {
                "videos": len(data["videos"]),
                "executions": len(data["executions"]),
                "corrections": len(data["corrections"]),
            },
        }
