"use client"

import type React from "react"

import { useState, useRef } from "react"
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
  Trash2,
  Play,
  Settings,
  BarChart3,
  Zap,
  User,
  LogOut,
} from "lucide-react"

export default function DashboardPage() {
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isUploading, setIsUploading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Mock user data
  const userData = {
    name: "John Doe",
    email: "john.doe@example.com",
    joinDate: "January 2024",
    scriptsGenerated: 12,
    totalUploadTime: "2.5 hours",
    successRate: "98%",
  }

  // Mock saved scripts data
  const savedScripts = [
    {
      id: 1,
      name: "Login Automation",
      created: "2024-01-15",
      duration: "5.2s",
      status: "completed",
      thumbnail: "/video-thumbnail.png",
    },
    {
      id: 2,
      name: "Form Submission",
      created: "2024-01-14",
      duration: "8.1s",
      status: "processing",
      thumbnail: "/video-thumbnail.png",
    },
    {
      id: 3,
      name: "Data Entry Workflow",
      created: "2024-01-12",
      duration: "12.5s",
      status: "completed",
      thumbnail: "/video-thumbnail.png",
    },
  ]

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

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error("Please select a video file first")
      return
    }

    setIsUploading(true)
    setUploadProgress(0)

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsUploading(false)
          toast.success("Video uploaded successfully! Processing automation script...")
          setSelectedFile(null)
          return 100
        }
        return prev + 10
      })
    }, 300)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

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
          <Button variant="outline" className="gap-2 bg-transparent">
            <LogOut className="size-4" />
            Sign Out
          </Button>
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
                          Processing...
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

            {/* Recent Scripts */}
            <Card className="border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileVideo className="size-5" />
                  Recent Scripts
                </CardTitle>
                <CardDescription>Your latest automation scripts</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {savedScripts.map((script) => (
                    <div
                      key={script.id}
                      className="flex items-center gap-4 p-4 rounded-lg border border-primary/10 hover:border-primary/30 transition-colors"
                    >
                      <img
                        src={script.thumbnail || "/placeholder.svg"}
                        alt={script.name}
                        className="w-20 h-15 rounded object-cover bg-primary/10"
                      />
                      <div className="flex-1">
                        <h3 className="font-semibold">{script.name}</h3>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground mt-1">
                          <div className="flex items-center gap-1">
                            <Calendar className="size-3" />
                            {script.created}
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="size-3" />
                            {script.duration}
                          </div>
                          <Badge variant={script.status === "completed" ? "default" : "secondary"} className="text-xs">
                            {script.status}
                          </Badge>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button variant="ghost" size="sm">
                          <Play className="size-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Download className="size-4" />
                        </Button>
                        <Button variant="ghost" size="sm" className="text-destructive hover:text-destructive">
                          <Trash2 className="size-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* User Stats */}
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

            {/* Quick Actions */}
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

            {/* Usage Tips */}
            <Card className="border-primary/20">
              <CardHeader>
                <CardTitle>Pro Tips</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                <div className="p-3 rounded-lg bg-primary/5 border border-primary/20">
                  <p className="font-medium text-primary mb-1">Better Quality</p>
                  <p className="text-muted-foreground">Record in 1080p for more accurate automation scripts</p>
                </div>
                <div className="p-3 rounded-lg bg-primary/5 border border-primary/20">
                  <p className="font-medium text-primary mb-1">Clear Actions</p>
                  <p className="text-muted-foreground">Make deliberate, slow movements for better detection</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
