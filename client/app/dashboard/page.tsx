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
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

import { toast } from "sonner";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import AutomationStatus from "@/components/AutomationStatus";
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
  Plus,
  Trash2,
  Key,
  Check,
} from "lucide-react";

interface Credential {
  id: string;
  label: string;
  username: string;
  password: string;
  apiKey: string;
  notes: string;
}

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
  const [credentials, setCredentials] = useState<Credential[]>([]);
  const [isRunningScript, setIsRunningScript] = useState(false);
  const [isDragActive, setIsDragActive] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const steps = [
    {
      number: 1,
      title: "Upload Video",
      description: "Record and upload your screen",
    },
    { number: 2, title: "Analysis", description: "Extract actions from video" },
    {
      number: 3,
      title: "Credentials",
      description: "Add login details (optional)",
    },
    {
      number: 4,
      title: "Generate Script",
      description: "Create automation script",
    },
  ];

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
    if (file) {
      if (file.type.startsWith("video/")) {
        setSelectedFile(file);
        toast.success(`Selected: ${file.name}`);
      } else {
        toast.error("Please select a video file");
      }
    }
    if (event.target) {
      event.target.value = "";
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  };

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!e.currentTarget.contains(e.relatedTarget as Node)) {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    const files = e.dataTransfer.files;
    const file = files[0];

    if (file) {
      if (file.type.startsWith("video/")) {
        setSelectedFile(file);
        toast.success(`Selected: ${file.name}`);
      } else {
        toast.error("Please drop a video file");
      }
    } else {
      toast.error("No file was dropped");
    }
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
      setUploadProgress(100);
      toast.success("Video uploaded successfully!");

      localStorage.setItem("lastVideoId", uploadedVideo.video_id);

      setTimeout(() => {
        setCurrentStep(2);
        setIsUploading(false);
        setUploadProgress(0);
      }, 1000);
    } catch (err: any) {
      toast.error(err.message || "Upload failed");
      setIsUploading(false);
      setUploadProgress(0);
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
      // Show message about browser automation
      toast.success("🎬 Starting analysis and browser automation demo!");
      
      const triggerRes = await fetch(
        `http://localhost:8000/api/automation/trigger/${videoId}`,
        {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (!triggerRes.ok) throw new Error("Failed to trigger extraction");
      
      // Show browser automation message
      setTimeout(() => {
        toast.success("🚀 Browser window should open for automation demo!");
      }, 2000);

      let status = "processing";
      while (status === "processing" || status === "queued") {
        await new Promise((resolve) => setTimeout(resolve, 3000));
        const statusRes = await fetch(
          `http://localhost:8000/api/automation/status/${videoId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const statusData = await statusRes.json();
        status = statusData.data?.analysis_status || "failed";
      }

      if (status !== "completed") throw new Error("Analysis failed");

      const resultsRes = await fetch(
        `http://localhost:8000/api/automation/results/${videoId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const resultsData = await resultsRes.json();

      // Extract the analysis data properly
      const analysisData = resultsData.data?.analysis || resultsData.data;
      const steps = analysisData?.steps || [];

      setAnalysisResult({
        detectedActions: steps.map(
          (step: any, index: number) =>
            `${index + 1}. ${step.action || step.type || "Action"}: ${
              step.description || step.selector || "Detected action"
            }`
        ),
        steps: steps,
        status: analysisData?.status || "completed",
      });

      toast.success(`Video analysis completed! Found ${steps.length} actions.`);
      setTimeout(() => setCurrentStep(3), 1000);
    } catch (err: any) {
      console.error(err);
      toast.error(err.message || "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const addCredential = () => {
    const newCredential: Credential = {
      id: Date.now().toString(),
      label: `Credential ${credentials.length + 1}`,
      username: "",
      password: "",
      apiKey: "",
      notes: "",
    };
    setCredentials([...credentials, newCredential]);
  };

  const updateCredential = (
    id: string,
    field: keyof Omit<Credential, "id">,
    value: string
  ) => {
    setCredentials(
      credentials.map((cred) =>
        cred.id === id ? { ...cred, [field]: value } : cred
      )
    );
  };

  const removeCredential = (id: string) => {
    setCredentials(credentials.filter((cred) => cred.id !== id));
  };

  const handleRunScript = async () => {
    setIsRunningScript(true);
    setTimeout(() => {
      setIsRunningScript(false);
      toast.success("Automation script generated successfully!");
      setTimeout(() => {
        setCurrentStep(1);
        setSelectedFile(null);
        setAnalysisResult(null);
        setCredentials([]);
        setUploadProgress(0);
      }, 1500);
    }, 2000);
  };

  const goToStep = (step: number) => {
    if (
      step <= currentStep ||
      (step === 2 && selectedFile) ||
      (step === 3 && analysisResult)
    ) {
      setCurrentStep(step);
    }
  };

  const canProceedToNext = () => {
    switch (currentStep) {
      case 1:
        return selectedFile !== null;
      case 2:
        return analysisResult !== null;
      case 3:
        return true; // Credentials are optional
      case 4:
        return false;
      default:
        return false;
    }
  };

  const initials = (name = "User") =>
    name
      .split(" ")
      .map((p) => p[0])
      .join("")
      .slice(0, 2)
      .toUpperCase();

  const successNumeric =
    parseInt(userData.successRate.replace("%", ""), 10) || 0;

  const cardBase =
    "rounded-2xl p-4 sm:p-6 bg-gradient-to-br from-black/60 to-black/50 border border-white/6 shadow-sm transition hover:shadow-lg";

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <Card className={`${cardBase} border-primary/12`}>
            <CardHeader>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4">
                <div className="flex items-center gap-3">
                  <Upload className="size-4 sm:size-5 text-primary flex-shrink-0" />
                  <div>
                    <CardTitle className="text-base sm:text-lg">
                      Upload a video
                    </CardTitle>
                    <CardDescription className="text-xs sm:text-sm">
                      Capture a screen recording — recommended 30s–3m
                    </CardDescription>
                  </div>
                </div>
                <Badge className="text-xs">Pro</Badge>
              </div>
            </CardHeader>

            <CardContent>
              <div
                className={`rounded-lg border-2 p-4 sm:p-6 text-center cursor-pointer transition-all duration-200 ${
                  isDragActive
                    ? "border-primary/60 bg-primary/5 scale-[1.02]"
                    : "border-dashed border-white/10 bg-transparent hover:border-white/20 hover:bg-white/2"
                }`}
                onDragOver={handleDragOver}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={(e) => {
                  if ((e.target as HTMLElement).closest("button")) return;
                  fileInputRef.current?.click();
                }}
              >
                <FileVideo className="mx-auto mb-3 size-8 sm:size-12 text-primary" />
                <h3 className="text-base sm:text-lg font-semibold mb-1">
                  {selectedFile
                    ? selectedFile.name
                    : "Drop your screen recording here"}
                </h3>
                <p className="text-xs sm:text-sm text-muted-foreground mb-4">
                  {selectedFile
                    ? `Size: ${(selectedFile.size / 1024 / 1024).toFixed(2)} MB`
                    : "Supports MP4, MOV, AVI, MKV"}
                </p>

                <div className="flex flex-col sm:flex-row items-center justify-center gap-2 sm:gap-3">
                  <Button
                    variant="outline"
                    size="sm"
                    type="button"
                    className="gap-1 sm:gap-2 bg-transparent w-full sm:w-auto text-xs sm:text-sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      fileInputRef.current?.click();
                    }}
                  >
                    Browse Files
                  </Button>

                  <Button
                    size="sm"
                    type="button"
                    className="gap-1 sm:gap-2 w-full sm:w-auto text-xs sm:text-sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleUpload();
                    }}
                    disabled={isUploading || !selectedFile}
                  >
                    {isUploading ? "Uploading..." : "Upload & Analyze"}
                  </Button>
                </div>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept="video/*,video/mp4,video/mov,video/avi,video/mkv,video/webm"
                  onChange={handleFileSelect}
                  className="hidden"
                  multiple={false}
                />

                {isUploading && (
                  <div className="mt-4">
                    <Progress value={uploadProgress} className="h-1.5 sm:h-2" />
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        );

      case 2:
        return (
          <Card className={`${cardBase} border-primary/12`}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <Eye className="size-4 sm:size-5 text-primary" />
                <CardTitle className="text-base sm:text-lg">
                  Analysis Status
                </CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              {!analysisResult ? (
                <div className="py-4 sm:py-6">
                  <p className="text-xs sm:text-sm text-muted-foreground mb-4">
                    Upload a recording and run analysis to extract actions.
                  </p>
                  <Button
                    onClick={handleAnalyze}
                    disabled={isAnalyzing}
                    className="w-full sm:w-auto"
                  >
                    {isAnalyzing ? "Analyzing..." : "Start Analysis"}
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center gap-2 text-green-400">
                    <CheckCircle className="size-5" />
                    <span className="font-medium">Analysis Complete</span>
                  </div>

                  <div className="space-y-3">
                    <h4 className="font-semibold text-sm sm:text-base">
                      Detected Actions
                    </h4>
                    <ul className="space-y-2">
                      {analysisResult.detectedActions?.map(
                        (action: string, idx: number) => (
                          <li
                            key={idx}
                            className="flex items-center gap-2 text-xs sm:text-sm"
                          >
                            <CheckCircle className="size-3 sm:size-4 text-primary flex-shrink-0" />
                            {action}
                          </li>
                        )
                      ) || (
                        <li className="text-xs sm:text-sm text-muted-foreground">
                          Click, Type, Navigate, Scroll actions detected
                        </li>
                      )}
                    </ul>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        );

      case 3:
        return (
          <Card className={`${cardBase} border-primary/12`}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Key className="size-4 sm:size-5 text-primary" />
                  <div>
                    <CardTitle className="text-base sm:text-lg">
                      Credentials (Optional)
                    </CardTitle>
                    <CardDescription className="text-xs sm:text-sm">
                      Add login details for automation
                    </CardDescription>
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={addCredential}
                  className="gap-2 bg-transparent"
                >
                  <Plus className="size-4" />
                  Add
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {credentials.length === 0 ? (
                <div className="py-6 text-center">
                  <Key className="mx-auto mb-3 size-12 text-muted-foreground/50" />
                  <p className="text-sm text-muted-foreground mb-4">
                    No credentials added. You can skip this step or add login
                    details for automated form filling.
                  </p>
                  <Button
                    onClick={addCredential}
                    variant="outline"
                    className="bg-transparent"
                  >
                    <Plus className="size-4 mr-2" />
                    Add First Credential
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {credentials.map((credential) => (
                    <div
                      key={credential.id}
                      className="p-4 rounded-lg border border-white/10 bg-white/2 space-y-3"
                    >
                      <div className="flex items-center justify-between">
                        <Input
                          placeholder="Credential Label (e.g., Gmail, GitHub)"
                          value={credential.label}
                          onChange={(e) =>
                            updateCredential(
                              credential.id,
                              "label",
                              e.target.value
                            )
                          }
                          className="bg-transparent border-white/10 text-sm"
                        />
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeCredential(credential.id)}
                          className="text-red-400 hover:text-red-300"
                        >
                          <Trash2 className="size-4" />
                        </Button>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                          <Label
                            htmlFor={`username-${credential.id}`}
                            className="text-xs text-muted-foreground"
                          >
                            Username/Email
                          </Label>
                          <Input
                            id={`username-${credential.id}`}
                            placeholder="username@example.com"
                            value={credential.username}
                            onChange={(e) =>
                              updateCredential(
                                credential.id,
                                "username",
                                e.target.value
                              )
                            }
                            className="bg-transparent border-white/10 text-sm mt-1"
                          />
                        </div>
                        <div>
                          <Label
                            htmlFor={`password-${credential.id}`}
                            className="text-xs text-muted-foreground"
                          >
                            Password
                          </Label>
                          <Input
                            id={`password-${credential.id}`}
                            type="password"
                            placeholder="••••••••"
                            value={credential.password}
                            onChange={(e) =>
                              updateCredential(
                                credential.id,
                                "password",
                                e.target.value
                              )
                            }
                            className="bg-transparent border-white/10 text-sm mt-1"
                          />
                        </div>
                      </div>

                      <div>
                        <Label
                          htmlFor={`apikey-${credential.id}`}
                          className="text-xs text-muted-foreground"
                        >
                          API Key (if needed)
                        </Label>
                        <Input
                          id={`apikey-${credential.id}`}
                          placeholder="sk-..."
                          value={credential.apiKey}
                          onChange={(e) =>
                            updateCredential(
                              credential.id,
                              "apiKey",
                              e.target.value
                            )
                          }
                          className="bg-transparent border-white/10 text-sm mt-1"
                        />
                      </div>

                      <div>
                        <Label
                          htmlFor={`notes-${credential.id}`}
                          className="text-xs text-muted-foreground"
                        >
                          Notes
                        </Label>
                        <Textarea
                          id={`notes-${credential.id}`}
                          placeholder="Additional notes..."
                          value={credential.notes}
                          onChange={(e) =>
                            updateCredential(
                              credential.id,
                              "notes",
                              e.target.value
                            )
                          }
                          className="bg-transparent border-white/10 text-sm mt-1 min-h-[60px]"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        );

      case 4:
        return (
          <Card className={`${cardBase} border-primary/12`}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <PlayCircle className="size-4 sm:size-5 text-primary" />
                <CardTitle className="text-base sm:text-lg">
                  Generate Script
                </CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 rounded-lg bg-white/5 border border-white/10">
                  <h4 className="font-medium mb-2">
                    Ready to generate automation script
                  </h4>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    <li className="flex items-center gap-2">
                      <Check className="size-4 text-green-400" />
                      Video analyzed:{" "}
                      {analysisResult?.detectedActions?.length || 0} actions
                      found
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="size-4 text-green-400" />
                      Credentials: {credentials.length} added
                    </li>
                  </ul>
                </div>

                <Button
                  onClick={handleRunScript}
                  disabled={isRunningScript}
                  className="w-full"
                >
                  {isRunningScript
                    ? "Generating Script..."
                    : "Generate & Run Script"}
                </Button>

                <div className="text-center">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => toast("Script history coming soon")}
                  >
                    View History
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />

      <div className="max-w-6xl mx-auto mt-10 px-4 sm:px-6 py-8 sm:py-12">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8 sm:mb-10">
          <div className="flex items-center gap-3 sm:gap-4">
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-purple-600 to-cyan-500 flex items-center justify-center text-white font-semibold shadow text-sm sm:text-base">
              {initials(userData.name)}
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold">
                Welcome back, {userData.name}
              </h1>
              <p className="text-xs sm:text-sm text-muted-foreground">
                Member since {userData.joinDate}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            <Button
              variant="ghost"
              size="sm"
              className="text-xs sm:text-sm"
              onClick={() => window.location.reload()}
            >
              Refresh
            </Button>
          </div>
        </div>

        {/* Step Progress */}
        <Card className={`${cardBase} border-primary/12 mb-8`}>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              {steps.map((step, index) => (
                <div key={step.number} className="flex items-center">
                  <div
                    className={`flex items-center cursor-pointer transition-all ${
                      step.number <= currentStep
                        ? "text-primary"
                        : "text-muted-foreground"
                    }`}
                    onClick={() => goToStep(step.number)}
                  >
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium border-2 transition-all ${
                        step.number === currentStep
                          ? "bg-primary border-primary text-white"
                          : step.number < currentStep
                          ? "bg-primary/20 border-primary text-primary"
                          : "bg-transparent border-white/20 text-muted-foreground"
                      }`}
                    >
                      {step.number < currentStep ? (
                        <Check className="size-4" />
                      ) : (
                        step.number
                      )}
                    </div>
                    <div className="ml-3 hidden sm:block">
                      <div className="text-sm font-medium">{step.title}</div>
                      <div className="text-xs text-muted-foreground">
                        {step.description}
                      </div>
                    </div>
                  </div>

                  {index < steps.length - 1 && (
                    <div
                      className={`w-8 sm:w-16 h-0.5 mx-2 sm:mx-4 transition-all ${
                        step.number < currentStep ? "bg-primary" : "bg-white/10"
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Layout: responsive grid */}
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 xl:gap-10">
          {/* MAIN - step content */}
          <main className="xl:col-span-8 space-y-6 sm:space-y-8">
            {renderStepContent()}

            {/* Navigation */}
            <div className="flex justify-between">
              <Button
                variant="outline"
                onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
                disabled={currentStep === 1}
                className="gap-2 bg-transparent"
              >
                <ArrowLeft className="size-4" />
                Previous
              </Button>

              {currentStep < 4 && (
                <Button
                  onClick={() => setCurrentStep(currentStep + 1)}
                  disabled={!canProceedToNext()}
                  className="gap-2"
                >
                  Next
                  <ArrowRight className="size-4" />
                </Button>
              )}
            </div>

            {/* Recent uploads - only show on step 1 */}
            {currentStep === 1 && (
              <Card className={`${cardBase} border-primary/12`}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <FileVideo className="size-4 sm:size-5 text-primary" />
                    <CardTitle className="text-base sm:text-lg">
                      Recent uploads
                    </CardTitle>
                  </div>
                  <CardDescription className="text-xs sm:text-sm">
                    Latest videos and processing status
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {uploadedVideos.length === 0 ? (
                    <div className="py-6 sm:py-8 text-center text-muted-foreground">
                      <p className="text-sm sm:text-base">
                        No videos uploaded yet.
                      </p>
                      <p className="mt-2 text-xs sm:text-sm">
                        Upload a recording to start automating.
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {uploadedVideos.slice(0, 3).map((video, idx) => (
                        <div
                          key={idx}
                          className="flex items-center justify-between gap-2 sm:gap-4 p-2 sm:p-3 rounded-lg bg-white/3"
                        >
                          <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
                            {video.thumbnail ? (
                              <img
                                src={video.thumbnail}
                                alt="thumb"
                                className="w-10 h-7 sm:w-14 sm:h-10 object-cover rounded-md flex-shrink-0"
                              />
                            ) : (
                              <div className="w-10 h-7 sm:w-14 sm:h-10 rounded-md bg-white/5 flex items-center justify-center flex-shrink-0">
                                <FileVideo className="w-3 h-3 sm:w-4 sm:h-4" />
                              </div>
                            )}
                            <div className="min-w-0 flex-1">
                              <div className="font-medium text-xs sm:text-sm truncate">
                                {video.original_name || "Untitled"}
                              </div>
                              <div className="text-xs text-muted-foreground mt-0.5 sm:mt-1">
                                <span className="block sm:inline">
                                  {(video.upload_timestamp &&
                                    new Date(
                                      video.upload_timestamp
                                    ).toLocaleDateString()) ||
                                    "—"}
                                </span>
                                <span className="hidden sm:inline"> • </span>
                                <span className="block sm:inline">
                                  {video.duration || "—"}
                                </span>
                              </div>
                            </div>
                          </div>

                          <div className="flex items-center gap-1 sm:gap-3 flex-shrink-0">
                            <Badge
                              variant={
                                video.status === "completed"
                                  ? "default"
                                  : "secondary"
                              }
                              className="text-xs"
                            >
                              {video.status || "processing"}
                            </Badge>
                            <Dialog>
                              <DialogTrigger asChild>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="p-1 sm:p-2"
                                >
                                  <Eye className="w-3 h-3 sm:w-4 sm:h-4" />
                                </Button>
                              </DialogTrigger>
                              <DialogContent className="max-w-2xl">
                                <DialogHeader>
                                  <DialogTitle>
                                    Automation Status - {video.original_name}
                                  </DialogTitle>
                                </DialogHeader>
                                <AutomationStatus
                                  videoId={video.video_id}
                                  onExecute={() => {
                                    toast.success(
                                      "Automation started! Check status for updates."
                                    );
                                  }}
                                />
                              </DialogContent>
                            </Dialog>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </main>

          {/* SIDEBAR - profile and quick actions */}
          <aside className="xl:col-span-4">
            <div className="space-y-4 sm:space-y-6">
              <Card className={`${cardBase} border-primary/12`}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <User className="size-4 sm:size-5 text-primary" />
                    <CardTitle className="text-base sm:text-lg">
                      Profile
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-3 min-w-0 flex-1">
                      <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-purple-600 to-cyan-500 flex items-center justify-center text-white font-semibold text-sm sm:text-base flex-shrink-0">
                        {initials(userData.name)}
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="font-medium text-sm sm:text-base truncate">
                          {userData.name}
                        </div>
                        <div className="text-xs sm:text-sm text-muted-foreground truncate">
                          {userData.email}
                        </div>
                      </div>
                    </div>

                    <div className="text-center flex-shrink-0">
                      <div className="w-16 h-16 sm:w-20 sm:h-20">
                        <svg className="w-full h-full" viewBox="0 0 80 80">
                          <circle
                            cx="40"
                            cy="40"
                            r="30"
                            stroke="rgba(255,255,255,0.06)"
                            strokeWidth="8"
                            fill="none"
                          />
                          <circle
                            cx="40"
                            cy="40"
                            r="30"
                            stroke="url(#g)"
                            strokeWidth="8"
                            strokeDasharray={`${
                              (successNumeric / 100) * 188
                            } 188`}
                            strokeLinecap="round"
                            transform="rotate(-90 40 40)"
                          />
                          <defs>
                            <linearGradient id="g">
                              <stop offset="0%" stopColor="#06b6d4" />
                              <stop offset="100%" stopColor="#6d28d9" />
                            </linearGradient>
                          </defs>
                          <text
                            x="40"
                            y="45"
                            textAnchor="middle"
                            fill="#fff"
                            fontSize="12"
                            fontWeight="600"
                            className="sm:text-sm"
                          >
                            {userData.successRate}
                          </text>
                        </svg>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-2 sm:gap-3 text-center mt-4">
                    <div>
                      <div className="text-xs text-muted-foreground">
                        Scripts
                      </div>
                      <div className="font-bold text-sm sm:text-lg text-primary">
                        {userData.scriptsGenerated}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">
                        Upload time
                      </div>
                      <div className="font-bold text-sm sm:text-lg text-primary">
                        {userData.totalUploadTime}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground">
                        Joined
                      </div>
                      <div className="font-bold text-sm sm:text-lg">
                        {userData.joinDate.split("/").slice(0, 2).join("/")}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className={`${cardBase} border-primary/12`}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <Settings className="size-4 sm:size-5 text-primary" />
                    <CardTitle className="text-base sm:text-lg">
                      Quick Actions
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-2 sm:space-y-3">
                  <Button
                    variant="outline"
                    className="w-full justify-start gap-2 sm:gap-3 bg-transparent text-xs sm:text-sm"
                    onClick={() => toast("Opening analytics...")}
                  >
                    <BarChart3 className="w-3 h-3 sm:w-4 sm:h-4" />
                    View Analytics
                  </Button>
                  <Button
                    variant="outline"
                    className="w-full justify-start gap-2 sm:gap-3 bg-transparent text-xs sm:text-sm"
                    onClick={() => toast("Opening settings...")}
                  >
                    <Settings className="w-3 h-3 sm:w-4 sm:h-4" />
                    Account Settings
                  </Button>
                  <Button
                    variant="ghost"
                    className="w-full justify-start gap-2 sm:gap-3 text-xs sm:text-sm"
                    onClick={() => toast("Invite flow coming soon")}
                  >
                    <ArrowRight className="w-3 h-3 sm:w-4 sm:h-4" />
                    Invite Teammates
                  </Button>
                </CardContent>
              </Card>

              {/* Current Step Summary */}
              <Card className={`${cardBase} border-primary/12`}>
                <CardHeader>
                  <CardTitle className="text-base sm:text-lg">
                    Current Progress
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Step {currentStep} of 4</span>
                      <span className="text-xs text-muted-foreground">
                        {Math.round((currentStep / 4) * 100)}%
                      </span>
                    </div>
                    <Progress value={(currentStep / 4) * 100} className="h-2" />
                    <div className="text-xs text-muted-foreground">
                      {steps.find((s) => s.number === currentStep)?.description}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
