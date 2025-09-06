"use client"

import type React from "react"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { toast } from "sonner"
import { ArrowLeft, Sparkles } from "lucide-react"
import { BackgroundBeams } from "@/components/ui/background-beams"
import SignupFormDemo from "@/components/signup-form-demo"
import Link from "next/link"

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState("signin")
  const router = useRouter()

  // Base URL of your Flask backend
  const API_URL = "http://localhost:8000/api/auth"

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    const email = formData.get("email") as string
    const password = formData.get("password") as string

    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.message || "Login failed")
      }

      const data = await res.json()
      console.log(data.data.user.name)
      // Save token/user info
      localStorage.setItem("isLoggedIn", "true")
      localStorage.setItem("userEmail", data.data.user.email)
      localStorage.setItem("userName", data.data.user.name)
      localStorage.setItem("token", data.data.token)

      window.dispatchEvent(new Event("storage"))

      toast.success("Successfully signed in!")
      router.push("/dashboard")
    } catch (err: any) {
      toast.error(err.message || "Error signing in")
    }
  }

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    const name = formData.get("name") as string
    const email = formData.get("email") as string
    const password = formData.get("password") as string

    try {
      const res = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.message || "Signup failed")
      }

      const data = await res.json()

      // Save token/user info
      localStorage.setItem("isLoggedIn", "true")
      localStorage.setItem("userEmail", email)
      localStorage.setItem("userName", name)
      localStorage.setItem("token", data.token)

      window.dispatchEvent(new Event("storage"))

      toast.success("Account created successfully!")
      router.push("/dashboard")
    } catch (err: any) {
      toast.error(err.message || "Error creating account")
    }
  }

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      <BackgroundBeams />

      <div className="absolute top-6 left-6 z-10">
        <Link
          href="/"
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/20 dark:bg-white/10 backdrop-blur-sm border border-white/30 dark:border-white/20 text-gray-700 dark:text-gray-300 hover:bg-white/30 dark:hover:bg-white/15 transition-all duration-200"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>
      </div>

      <div className="min-h-screen flex">
        {/* Left side - Branding */}
        <div className="flex-1 flex items-center justify-center p-8 relative z-10">
          <div className="max-w-md text-center relative">
            <div className="absolute inset-0 bg-white/10 dark:bg-white/5 backdrop-blur-xl rounded-3xl border border-white/20 dark:border-white/10 shadow-2xl" />
            <div className="relative z-10 p-8">
              <div className="flex items-center justify-center gap-3 mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center shadow-lg">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-3xl font-bold text-gray-800 dark:text-white">Mimicker AI</h1>
              </div>
              <p className="text-lg text-gray-700 dark:text-gray-200 leading-relaxed">
                Create your digital identity and connect with your audience like never before. Transform screen
                recordings into powerful automation scripts with AI.
              </p>
            </div>
          </div>
        </div>

        {/* Right side - Form */}
        <div className="flex-1 flex items-center justify-center p-8 relative z-10">
          <div className="w-full max-w-md">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-8 bg-white/20 dark:bg-white/10 backdrop-blur-sm border border-white/30 dark:border-white/20">
                <TabsTrigger
                  value="signin"
                  className="data-[state=active]:bg-white/40 dark:data-[state=active]:bg-white/20 text-gray-700 dark:text-gray-200"
                >
                  Sign In
                </TabsTrigger>
                <TabsTrigger
                  value="signup"
                  className="data-[state=active]:bg-white/40 dark:data-[state=active]:bg-white/20 text-gray-700 dark:text-gray-200"
                >
                  Sign Up
                </TabsTrigger>
              </TabsList>

              <TabsContent value="signin">
                <SignupFormDemo onSubmit={handleSignIn} isSignUp={false} />
              </TabsContent>

              <TabsContent value="signup">
                <SignupFormDemo onSubmit={handleSignUp} isSignUp={true} />
              </TabsContent>
            </Tabs>

            <div className="text-center mt-6">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                By continuing, you agree to our{" "}
                <Link href="/terms" className="text-blue-600 dark:text-blue-400 hover:underline">
                  Terms of Service
                </Link>{" "}
                and{" "}
                <Link href="/privacy" className="text-blue-600 dark:text-blue-400 hover:underline">
                  Privacy Policy
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
