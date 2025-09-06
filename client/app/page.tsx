"use client"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Navigation } from "@/components/navigation"
import { toast } from "sonner"
import { Sparkles, ArrowRight, Code, Globe, Brain, Shield } from "lucide-react"

type ProcessingStep = "upload" | "analyzing" | "generating" | "complete"

export default function MimickerAI() {
  const [currentStep, setCurrentStep] = useState<ProcessingStep>("upload")
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [generatedScript, setGeneratedScript] = useState("")
  const [copied, setCopied] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setUploadedFile(file)
      toast.success("Video uploaded successfully!")
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "video/*": [".mp4", ".mov", ".avi", ".mkv"],
    },
    maxFiles: 1,
  })

  const processVideo = async () => {
    if (!uploadedFile) return

    setCurrentStep("analyzing")

    // Simulate processing steps
    setTimeout(() => setCurrentStep("generating"), 2000)
    setTimeout(() => {
      setCurrentStep("complete")
      setGeneratedScript(`{
  "name": "Web Automation Script",
  "version": "1.0.0",
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com",
      "wait": 2000
    },
    {
      "action": "click",
      "selector": "#login-button",
      "description": "Click login button"
    },
    {
      "action": "type",
      "selector": "#email",
      "text": "user@example.com",
      "description": "Enter email address"
    },
    {
      "action": "type",
      "selector": "#password",
      "text": "password123",
      "description": "Enter password"
    },
    {
      "action": "click",
      "selector": "#submit",
      "description": "Submit login form"
    }
  ]
}`)
      toast.success("Automation script generated!")
    }, 4000)
  }

  const copyScript = () => {
    navigator.clipboard.writeText(generatedScript)
    setCopied(true)
    toast.success("Script copied to clipboard!")
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadScript = () => {
    const blob = new Blob([generatedScript], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "automation-script.json"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    toast.success("Script downloaded!")
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />

      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 px-4">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-background to-accent/5" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/20 border border-primary/30 mb-8 animate-pulse-glow">
            <Sparkles className="size-4 text-foreground" />
            <span className="text-sm font-medium text-foreground">AI-Powered Automation</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold mb-6 text-balance">
            <span className="text-foreground drop-shadow-lg animate-gradient">Mimicker AI</span>
          </h1>

          <p className="text-xl md:text-2xl text-muted-foreground mb-12 text-balance max-w-2xl mx-auto">
            Automate web tasks by showing, not coding. Upload your screen recording and let AI generate the automation
            script.
          </p>

          <Button
            size="lg"
            className="animate-pulse-glow hover:scale-105 transition-transform duration-200"
            onClick={() => (window.location.href = "/profile")}
          >
            Get Started
            <ArrowRight className="ml-2 size-4" />
          </Button>
        </div>

        {/* Floating Elements */}
        <div className="absolute top-20 left-10 animate-float">
          <div className="size-20 rounded-full bg-primary/20 blur-xl" />
        </div>
        <div className="absolute bottom-20 right-10 animate-float" style={{ animationDelay: "1s" }}>
          <div className="size-16 rounded-full bg-accent/20 blur-xl" />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-muted/20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Why Choose Mimicker AI?</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Transform your manual workflows into automated scripts with the power of AI
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: Code,
                title: "No Coding Required",
                description: "Simply record your actions and let AI generate the automation script for you",
              },
              {
                icon: Globe,
                title: "Works Anywhere",
                description: "Compatible with any website or web application you can interact with",
              },
              {
                icon: Brain,
                title: "Smart AI Analysis",
                description: "Advanced computer vision and NLP to understand your actions perfectly",
              },
              {
                icon: Shield,
                title: "JSON Scripts",
                description: "Clean, readable JSON output that's easy to modify and integrate",
              },
            ].map((feature, index) => (
              <Card
                key={index}
                className="border-primary/20 hover:border-primary/40 transition-all duration-300 hover:scale-105"
              >
                <CardHeader className="text-center">
                  <div className="size-12 rounded-lg bg-primary/10 flex items-center justify-center mx-auto mb-4">
                    <feature.icon className="size-6 text-primary" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-center">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-to-br from-primary/10 via-background to-accent/5 rounded-2xl p-12 border border-primary/20">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to Automate Your Workflow?</h2>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Join thousands of users who have already automated their repetitive tasks with Mimicker AI
            </p>
            <Button
              size="lg"
              className="animate-pulse-glow hover:scale-105 transition-transform duration-200"
              onClick={() => (window.location.href = "/profile")}
            >
              Sign Up to Get Started
              <ArrowRight className="ml-2 size-4" />
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
