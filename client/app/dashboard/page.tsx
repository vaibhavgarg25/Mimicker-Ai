"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { toast } from "sonner"
import {
  Upload,
  FileVideo,
  Download,
  Calendar,
  Clock,
  Zap,
  User,
  Settings,
  BarChart3,
} from "lucide-react"

export default function DashboardPage() {
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isUploading, setIsUploading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploadedVideos, setUploadedVideos] = useState<any[]>([])
  const [userData, setUserData] = useState({
    name: "",
    email: "",
    joinDate: "",
    scriptsGenerated: 0,
    totalUploadTime: "0h",
    successRate: "0%",
  })

  const fileInputRef = useRef<HTMLInputElement>(null)

  // Fetch user data from localStorage
  useEffect(() => {
    const userName = localStorage.getItem("userName")
    const userEmail = localStorage.getItem("userEmail")
    const joinDate = localStorage.getItem("joinDate") || new Date().toLocaleDateString()
    setUserData((prev) => ({
      ...prev,
      name: userName || "User",
      email: userEmail || "",
      joinDate, 
      scriptsGenerated: 5, 
      totalUploadTime: "1.5h",
      successRate: "90%",
    })) 
    
  }, [])

  // Fetch videos from backend
  useEffect(() => {
    const fetchVideos = async () => {
      const token = localStorage.getItem("token")
      if (!token) return

      try {
        const res = await fetch("http://localhost:8000/api/videos/my-videos", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!res.ok) throw new Error("Failed to fetch videos")

        const data = await res.json()
        setUploadedVideos(data.data.videos || [])
      } catch (err) {
        console.error(err)
        toast.error("Could not load uploaded videos")
      }
    }

    fetchVideos()
  }, [])

  // Select file
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      if (file.type.startsWith("video/")) {
        setSelectedFile(file)
        toast.success(`Selected: ${file.name}`)
      } else {
        toast.error("Please select a video file")
      }
    }
  }

  // Upload file
  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error("Please select a video file first")
      return
    }

    const token = localStorage.getItem("token")
    if (!token) {
      toast.error("You must be signed in to upload")
      return
    }

    setIsUploading(true)
    setUploadProgress(0)

    const formData = new FormData()
    formData.append("video", selectedFile)

    const xhr = new XMLHttpRequest()
    xhr.open("POST", "http://localhost:8000/api/videos/upload", true)
    xhr.setRequestHeader("Authorization", `Bearer ${token}`)

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percentComplete = Math.round((event.loaded / event.total) * 100)
        setUploadProgress(percentComplete)
      }
    }

    xhr.onload = () => {
      setIsUploading(false)
      if (xhr.status === 201) {
        toast.success("Video uploaded successfully!")
        const response = JSON.parse(xhr.responseText)

        // Add new video from backend response
        setUploadedVideos((prev) => [response.data, ...prev])
        setSelectedFile(null)
        setUploadProgress(100)
      } else {
        const response = JSON.parse(xhr.responseText || "{}")
        toast.error(response.message || "Upload failed")
      }
    }

    xhr.onerror = () => {
      setIsUploading(false)
      toast.error("Upload failed. Please try again.")
    }

    xhr.send(formData)
  }

  // Drag & drop
  const handleDragOver = (e: React.DragEvent) => e.preventDefault()

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith("video/")) {
      setSelectedFile(file)
      toast.success(`Selected: ${file.name}`)
    } else {
      toast.error("Please drop a video file")
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        {/* Dashboard Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
            <p className="text-muted-foreground mt-1">Welcome back, {userData.name}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Upload Section */}
            <Card className="border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="size-5" />
                  Upload Video
                </CardTitle>
                <CardDescription>Upload a video to generate automation scripts</CardDescription>
              </CardHeader>
              <CardContent>
                <div
                  className="border-2 border-dashed border-primary/30 rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <FileVideo className="size-12 mx-auto mb-4 text-primary" />
                  <h3 className="text-lg font-semibold mb-2">
                    {selectedFile ? selectedFile.name : "Drop your video here"}
                  </h3>
                  <p className="text-muted-foreground mb-4">
                    {selectedFile
                      ? `File size: ${(selectedFile.size / 1024 / 1024).toFixed(2)} MB`
                      : "Supports MP4, AVI, MOV files up to 100MB"}
                  </p>
                  <Button variant="outline" className="gap-2 bg-transparent">
                    <Upload className="size-4" />
                    {selectedFile ? "Change File" : "Browse Files"}
                  </Button>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="video/*"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                </div>

                {selectedFile && (
                  <div className="mt-6">
                    <Button onClick={handleUpload} disabled={isUploading} className="w-full gap-2">
                      {isUploading ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                          Uploading...
                        </>
                      ) : (
                        <>
                          <Zap className="size-4" />
                          Generate Automation Script
                        </>
                      )}
                    </Button>

                    {isUploading && (
                      <div className="mt-4">
                        <div className="flex justify-between text-sm mb-2">
                          <span>Uploading...</span>
                          <span>{uploadProgress}%</span>
                        </div>
                        <Progress value={uploadProgress} className="h-2" />
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Recent Uploads */}
            <Card className="border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileVideo className="size-5" />
                  Recent Uploads
                </CardTitle>
                <CardDescription>Your uploaded videos</CardDescription>
              </CardHeader>
              <CardContent>
                {uploadedVideos.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No videos uploaded yet.</p>
                ) : (
                  <div className="space-y-4">
                    {uploadedVideos.map((video, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between p-4 rounded-lg border border-primary/10 hover:border-primary/30 transition-colors"
                      >
                        <div>
                          <h3 className="font-semibold">{video.original_name}</h3>
                          <div className="flex items-center gap-4 text-sm text-muted-foreground mt-1">
                            <div className="flex items-center gap-1">
                              <Calendar className="size-3" />
                              {video.upload_timestamp
                                ? new Date(video.upload_timestamp).toLocaleDateString()
                                : new Date().toLocaleDateString()}
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="size-3" />
                              {video.duration || "—"}
                            </div>
                          </div>
                        </div>
                        <Badge
                          variant={video.status === "completed" ? "default" : "secondary"}
                          className="text-xs"
                        >
                          {video.status || "processing"}
                        </Badge>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card className="border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="size-5" />
                  Profile Stats
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{userData.scriptsGenerated}</div>
                  <div className="text-sm text-muted-foreground">Scripts Generated</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{userData.totalUploadTime}</div>
                  <div className="text-sm text-muted-foreground">Total Upload Time</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{userData.successRate}</div>
                  <div className="text-sm text-muted-foreground">Success Rate</div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="size-5" />
                  Quick Actions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start gap-2 bg-transparent">
                  <BarChart3 className="size-4" />
                  View Analytics
                </Button>
                <Button variant="outline" className="w-full justify-start gap-2 bg-transparent">
                  <Settings className="size-4" />
                  Account Settings
                </Button>
                <Button variant="outline" className="w-full justify-start gap-2 bg-transparent">
                  <Download className="size-4" />
                  Export All Scripts
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
