import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

try:
    from pymongo import MongoClient
except ModuleNotFoundError:
    MongoClient = None

load_dotenv()

client = None
db = None


def _serialize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return {"__type__": "datetime", "value": value.isoformat()}
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize_value(item) for key, item in value.items()}
    return value


def _deserialize_value(value: Any) -> Any:
    if isinstance(value, dict) and value.get("__type__") == "datetime":
        return datetime.fromisoformat(value["value"])
    if isinstance(value, list):
        return [_deserialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _deserialize_value(item) for key, item in value.items()}
    return value


class LocalInsertResult:
    def __init__(self, inserted_id: str):
        self.inserted_id = inserted_id


class LocalUpdateResult:
    def __init__(self, modified_count: int):
        self.modified_count = modified_count


class LocalCollection:
    def __init__(self, store: "LocalDatabase", name: str):
        self.store = store
        self.name = name

    def create_index(self, *_args, **_kwargs):
        return None

    def insert_one(self, document: Dict[str, Any]) -> LocalInsertResult:
        data = self.store._read()
        doc = _deserialize_value(_serialize_value(document))
        doc["_id"] = str(doc.get("_id") or uuid.uuid4().hex)
        data.setdefault(self.name, []).append(doc)
        self.store._write(data)
        return LocalInsertResult(doc["_id"])

    def find_one(self, query: Dict[str, Any]) -> Dict[str, Any] | None:
        for document in self.find(query):
            return document
        return None

    def find(self, query: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        data = self.store._read()
        documents = data.get(self.name, [])
        query = query or {}
        matched: List[Dict[str, Any]] = []

        for document in documents:
            if all(document.get(key) == value for key, value in query.items()):
                matched.append(_deserialize_value(_serialize_value(document)))

        return matched

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> LocalUpdateResult:
        data = self.store._read()
        documents = data.get(self.name, [])
        modified_count = 0
        set_values = update.get("$set", {})

        for document in documents:
            if all(document.get(key) == value for key, value in query.items()):
                for field, field_value in set_values.items():
                    document[field] = _deserialize_value(_serialize_value(field_value))
                modified_count = 1
                break

        self.store._write(data)
        return LocalUpdateResult(modified_count)


class LocalDatabase:
    mode = "local"

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(
                {
                    "users": [],
                    "videos": [],
                    "video_analyses": [],
                    "automation_executions": [],
                }
            )

    def __getattr__(self, name: str) -> LocalCollection:
        return LocalCollection(self, name)

    def _read(self) -> Dict[str, List[Dict[str, Any]]]:
        return _deserialize_value(json.loads(self.path.read_text()))

    def _write(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        self.path.write_text(json.dumps(_serialize_value(data), indent=2))


def init_db():
    global client, db

    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/mimicker_ai")
    prefer_mongo = os.getenv("USE_MONGO", "").lower() in {"1", "true", "yes"}

    if prefer_mongo and MongoClient is not None:
        try:
            client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=1000)
            db_name = "mimicker_ai"
            db = client[db_name]
            client.admin.command("ping")
            print(f"✓ Connected to MongoDB successfully (database: {db_name})")
            try:
                db.users.create_index("email", unique=True)
                print("✓ Database indexes created")
            except Exception as idx_error:
                print(f"⚠ Index creation warning: {idx_error}")
            return
        except Exception as exc:
            print(f"⚠ MongoDB unavailable, falling back to local storage: {exc}")
    elif not prefer_mongo:
        print("✓ USE_MONGO not enabled, starting backend with local JSON storage")

    local_db_path = Path(
        os.getenv(
            "LOCAL_DB_PATH",
            Path(__file__).resolve().parent.parent / "data" / "local_db.json",
        )
    )
    db = LocalDatabase(local_db_path)
    client = None
    print(f"✓ Using local JSON database at {local_db_path}")


def get_db():
    return db
