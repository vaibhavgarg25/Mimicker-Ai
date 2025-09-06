"use client";

import type React from "react";
import { useState, useRef, useEffect } from "react";
import { Navigation } from "@/components/navigation";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";

import { toast } from "sonner";
import {
  Upload,
  FileVideo,

  User,
  Settings,
  BarChart3,
  CheckCircle,
  ArrowRight,
  ArrowLeft,

  PlayCircle,
  Eye,
} from "lucide-react";

export default function DashboardPage() {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadedVideos, setUploadedVideos] = useState<any[]>([]);
  const [userData, setUserData] = useState({
    name: "",
    email: "",
    joinDate: "",
    scriptsGenerated: 0,
    totalUploadTime: "0h",
    successRate: "0%",
  });

  const [currentStep, setCurrentStep] = useState(1);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
    apiKey: "",
    notes: "",
  });
  const [isRunningScript, setIsRunningScript] = useState(false);
  const [isDragActive, setIsDragActive] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const userName = localStorage.getItem("userName");
    const joinDate =
      localStorage.getItem("joinDate") || new Date().toLocaleDateString();
    setUserData((prev) => ({
      ...prev,
      name: userName || "User",
      email: localStorage.getItem("userEmail") || "",
      joinDate,
      scriptsGenerated: 5,
      totalUploadTime: "1.5h",
      successRate: "90%",
    }));
  }, []);

  useEffect(() => {
    const fetchVideos = async () => {
      const token = localStorage.getItem("token");
      if (!token) return;
      try {
        const res = await fetch("http://localhost:8000/api/videos/my-videos", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Failed to fetch videos");
        const data = await res.json();
        setUploadedVideos(data.data.videos || []);
      } catch (err) {
        console.error(err);
        toast.error("Could not load uploaded videos");
      }
    };
    fetchVideos();
  }, []);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith("video/")) {
      setSelectedFile(file);
      toast.success(`Selected: ${file.name}`);
    } else toast.error("Please select a video file");
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragActive(true);
  };
  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragActive(false);
  };
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragActive(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("video/")) {
      setSelectedFile(file);
      toast.success(`Selected: ${file.name}`);
    } else toast.error("Please drop a video file");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error("Please select a video first");
      return;
    }
    const token = localStorage.getItem("token");
    if (!token) {
      toast.error("You must be signed in");
      return;
    }

    setIsUploading(true);
    setUploadProgress(10);

    const formData = new FormData();
    formData.append("video", selectedFile);

    try {
      const res = await fetch("http://localhost:8000/api/videos/upload", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      const uploadedVideo = data.data;
      setUploadedVideos((prev) => [uploadedVideo, ...prev]);
      setSelectedFile(null);
      setUploadProgress(100);
      toast.success("Video uploaded successfully!");

      localStorage.setItem("lastVideoId", uploadedVideo.video_id);
      setCurrentStep(2);
    } catch (err: any) {
      toast.error(err.message || "Upload failed");
    } finally {
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
      }, 500);
    }
  };

  const handleAnalyze = async () => {
    const token = localStorage.getItem("token");
    const videoId = localStorage.getItem("lastVideoId");
    if (!token || !videoId) {
      toast.error("Missing token or video ID");
      return;
    }

    setIsAnalyzing(true);
    try {
      const triggerRes = await fetch(
        `http://localhost:8000/api/extraction/extract/${videoId}`,
        {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (!triggerRes.ok) throw new Error("Failed to trigger extraction");

      let status = "processing";
      while (status === "processing" || status === "queued") {
        await new Promise((resolve) => setTimeout(resolve, 3000));
        const statusRes = await fetch(
          `http://localhost:8000/api/extraction/status/${videoId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const statusData = await statusRes.json();
        status = statusData.data?.extraction_status || "failed";
      }

      if (status !== "completed") throw new Error("Extraction failed");

      const resultsRes = await fetch(
        `http://localhost:8000/api/extraction/results/${videoId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const resultsData = await resultsRes.json();

      setAnalysisResult(resultsData.data);
      toast.success("Video analysis completed!");
      setCurrentStep(3);
    } catch (err: any) {
      console.error(err);
      toast.error(err.message || "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRunScript = async () => {
    setIsRunningScript(true);
    setTimeout(() => {
      setIsRunningScript(false);
      toast.success("Automation script generated successfully!");
      setCurrentStep(1);
      setSelectedFile(null);
      setAnalysisResult(null);
      setCredentials({ username: "", password: "", apiKey: "", notes: "" });
      setUploadProgress(0);
    }, 1500);
  };

  const goToNextStep = () => {
    if (currentStep < 4) setCurrentStep(currentStep + 1);
  };
  const goToPreviousStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const initials = (name = "User") =>
    name
      .split(" ")
      .map((p) => p[0])
      .join("")
      .slice(0, 2)
      .toUpperCase();

  const successNumeric = parseInt(userData.successRate.replace("%", ""), 10) || 0;

  const cardBase =
    "rounded-2xl p-6 bg-gradient-to-br from-black/60 to-black/50 border border-white/6 shadow-sm transition hover:shadow-lg";

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />

      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-10">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-600 to-cyan-500 flex items-center justify-center text-white font-semibold shadow">
              {initials(userData.name)}
            </div>
            <div>
              <h1 className="text-2xl font-bold">Welcome back, {userData.name}</h1>
              <p className="text-sm text-muted-foreground">Member since {userData.joinDate}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button variant="ghost" onClick={() => window.location.reload()}>
              Refresh
            </Button>
            <Button onClick={() => fileInputRef.current?.click()}>
              <Upload /> New Upload
            </Button>
          </div>
        </div>

        {/* Layout: main + sidebar (narrow) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-y-8 gap-x-10">
          {/* MAIN - wider, stacked vertically for clarity */}
          <main className="lg:col-span-8 space-y-8">
            {/* Upload card (primary) */}
            <Card className={`${cardBase} border-primary/12`}>
              <CardHeader>
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <Upload className="size-5 text-primary" />
                    <div>
                      <CardTitle className="text-lg">Step 1 — Upload a video</CardTitle>
                      <CardDescription>Capture a screen recording — recommended 30s–3m</CardDescription>
                    </div>
                  </div>
                  <div>
                    <Badge>Pro</Badge>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                <div
                  className={`rounded-lg border-2 p-6 text-center cursor-pointer transition-colors ${
                    isDragActive ? "border-primary/60 bg-white/3" : "border-dashed border-white/10 bg-transparent"
                  }`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <FileVideo className="mx-auto mb-3 size-12 text-primary" />
                  <h3 className="text-lg font-semibold mb-1">
                    {selectedFile ? selectedFile.name : "Drop your screen recording here"}
                  </h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    {selectedFile ? `Size: ${(selectedFile.size / 1024 / 1024).toFixed(2)} MB` : "Supports MP4, MOV, AVI, MKV"}
                  </p>

                  <div className="flex items-center justify-center gap-3">
                    <Button variant="outline" className="gap-2 bg-transparent" onClick={() => fileInputRef.current?.click()}>
                      Browse files
                    </Button>

                    <Button onClick={handleUpload} disabled={isUploading || !selectedFile} className="gap-2">
                      {isUploading ? "Uploading..." : "Upload & Analyze"}
                    </Button>
                  </div>

                  <input ref={fileInputRef} type="file" accept="video/*" onChange={handleFileSelect} className="hidden" />

                  {isUploading && (
                    <div className="mt-4">
                      <Progress value={uploadProgress} className="h-2" />
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Analysis and Runner stacked for clarity */}
            <div className="space-y-6">
              <Card className={`${cardBase} border-primary/12`}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <Eye className="size-5 text-primary" />
                    <CardTitle className="text-lg">Analysis Status</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  {!analysisResult ? (
                    <div className="py-6">
                      <p className="text-sm text-muted-foreground mb-4">
                        No analysis results yet. Upload a recording and run analysis to extract actions.
                      </p>
                      <div className="flex gap-3">
                        <Button variant="outline" onClick={() => setCurrentStep(1)} className="bg-transparent">
                          <ArrowLeft /> Upload
                        </Button>
                        <Button onClick={handleAnalyze} disabled={isAnalyzing}>
                          {isAnalyzing ? "Analyzing..." : "Start analysis"}
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <h4 className="font-semibold">Detected actions</h4>
                      <ul className="space-y-2">
                        {analysisResult.detectedActions?.map((a: string, idx: number) => (
                          <li key={idx} className="flex items-center gap-2 text-sm">
                            <CheckCircle className="size-4 text-primary" />
                            {a}
                          </li>
                        )) || <li className="text-sm text-muted-foreground">No actions found</li>}
                      </ul>
                      <div className="flex justify-end">
                        <Button onClick={goToNextStep}>Continue</Button>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card className={`${cardBase} border-primary/12`}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <PlayCircle className="size-5 text-primary" />
                    <CardTitle className="text-lg">Script Runner</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">Generate and run automation scripts from your analysis.</p>
                  <div className="flex gap-3">
                    <Button onClick={handleRunScript} disabled={isRunningScript}>
                      {isRunningScript ? "Running..." : "Generate & Run"}
                    </Button>
                    <Button variant="ghost" onClick={() => toast("History coming soon")}>History</Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recent uploads */}
            <Card className={`${cardBase} border-primary/12`}>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <FileVideo className="size-5 text-primary" />
                  <CardTitle className="text-lg">Recent uploads</CardTitle>
                </div>
                <CardDescription>Latest videos and processing status</CardDescription>
              </CardHeader>
              <CardContent>
                {uploadedVideos.length === 0 ? (
                  <div className="py-8 text-center text-muted-foreground">
                    <p>No videos uploaded yet.</p>
                    <p className="mt-2 text-sm">Upload a recording to start automating.</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {uploadedVideos.slice(0, 6).map((video, idx) => (
                      <div key={idx} className="flex items-center justify-between gap-4 p-3 rounded-lg bg-white/3">
                        <div className="flex items-center gap-3">
                          {video.thumbnail ? (
                            <img src={video.thumbnail} alt="thumb" className="w-14 h-10 object-cover rounded-md" />
                          ) : (
                            <div className="w-14 h-10 rounded-md bg-white/5 flex items-center justify-center">
                              <FileVideo />
                            </div>
                          )}
                          <div>
                            <div className="font-medium">{video.original_name || "Untitled"}</div>
                            <div className="text-sm text-muted-foreground mt-1">
                              {(video.upload_timestamp && new Date(video.upload_timestamp).toLocaleString()) || "—"} • {video.duration || "—"}
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center gap-3">
                          <Badge variant={video.status === "completed" ? "default" : "secondary"}>
                            {video.status || "processing"}
                          </Badge>
                          <Button variant="ghost" size="sm" onClick={() => toast("Open player (not wired)")}>
                            <Eye />
                          </Button>
                        </div>
                      </div>
                    ))}
                    <div className="mt-4 text-right">
                      <Button variant="ghost" onClick={() => toast("View all uploads - route not wired")}>
                        View all uploads
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </main>

          {/* SIDEBAR - narrower, sticky, simpler */}
          <aside className="lg:col-span-4">
            <div className="space-y-6">
              <Card className={`${cardBase} border-primary/12`}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <User className="size-5 text-primary" />
                    <CardTitle className="text-lg">Profile</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-600 to-cyan-500 flex items-center justify-center text-white font-semibold">
                        {initials(userData.name)}
                      </div>
                      <div>
                        <div className="font-medium">{userData.name}</div>
                        <div className="text-sm text-muted-foreground">{userData.email}</div>
                      </div>
                    </div>

                    <div className="text-center">
                      {/* small circular progress - simple visual */}
                      <div className="w-20 h-20">
                        <svg width="80" height="80" viewBox="0 0 80 80">
                          <circle cx="40" cy="40" r="30" stroke="rgba(255,255,255,0.06)" strokeWidth="8" fill="none" />
                          <circle cx="40" cy="40" r="30" stroke="url(#g)" strokeWidth="8" strokeDasharray={`${(successNumeric/100)*188} 188`} strokeLinecap="round" transform="rotate(-90 40 40)" />
                          <defs>
                            <linearGradient id="g"><stop offset="0%" stopColor="#06b6d4"/><stop offset="100%" stopColor="#6d28d9" /></linearGradient>
                          </defs>
                          <text x="40" y="45" textAnchor="middle" fill="#fff" fontSize="14" fontWeight="600">{userData.successRate}</text>
                        </svg>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-3 text-center mt-4">
                    <div>
                      <div className="text-sm text-muted-foreground">Scripts</div>
                      <div className="font-bold text-lg text-primary">{userData.scriptsGenerated}</div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">Upload time</div>
                      <div className="font-bold text-lg text-primary">{userData.totalUploadTime}</div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">Joined</div>
                      <div className="font-bold text-lg">{userData.joinDate}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className={`${cardBase} border-primary/12`}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <Settings className="size-5 text-primary" />
                    <CardTitle className="text-lg">Quick actions</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button variant="outline" className="w-full justify-start gap-3 bg-transparent" onClick={() => toast("Opening analytics...")}>
                    <BarChart3 />
                    View analytics
                  </Button>
                  <Button variant="outline" className="w-full justify-start gap-3 bg-transparent" onClick={() => toast("Opening settings...")}>
                    <Settings />
                    Account settings
                  </Button>
                  <Button variant="ghost" className="w-full justify-start gap-3" onClick={() => toast("Invite flow coming soon")}>
                    <ArrowRight />
                    Invite teammates
                  </Button>
                </CardContent>
              </Card>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
