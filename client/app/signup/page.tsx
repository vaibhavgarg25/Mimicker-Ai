"use client"

import type React from "react"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { toast } from "sonner"
import { Sparkles } from "lucide-react"
import { Plasma } from "@/components/Plasma/plasma"
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
    <div className="min-h-screen bg-[#050505] text-foreground relative overflow-hidden">
      <div className="absolute inset-0 -z-20">
        <Plasma color="#ff6b35" speed={0.6} direction="forward" scale={1.1} opacity={0.8} mouseInteractive={true} />
      </div>

      <div className="min-h-screen flex">
        {/* Left side - Branding */}
        <div className="flex-1 flex items-center justify-center p-8 relative z-10">
          <div className="max-w-md text-center relative">
            <div className="absolute inset-0 bg-foreground/5 backdrop-blur-xl rounded-3xl border border-foreground/10 shadow-2xl" />
            <div className="relative z-10 p-8">
              <div className="flex items-center justify-center gap-3 mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center shadow-lg">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-3xl font-thin tracking-[4px] text-foreground/95">MIMICKER</h1>
              </div>
              <p className="text-sm text-foreground/60 leading-relaxed">
                Automate web tasks by showing — not coding. Transform screen recordings into powerful automation scripts
                with AI.
              </p>
            </div>
          </div>
        </div>

        {/* Right side - Form */}
        <div className="flex-1 flex items-center justify-center p-8 relative z-10">
          <div className="w-full max-w-md">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-8 bg-foreground/10 backdrop-blur-sm border border-foreground/20">
                <TabsTrigger
                  value="signin"
                  className="data-[state=active]:bg-foreground/20 text-foreground/80 data-[state=active]:text-foreground"
                >
                  Sign In
                </TabsTrigger>
                <TabsTrigger
                  value="signup"
                  className="data-[state=active]:bg-foreground/20 text-foreground/80 data-[state=active]:text-foreground"
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
              <p className="text-xs text-foreground/40">
                By continuing, you agree to our{" "}
                <Link href="/terms" className="text-orange-400 hover:text-orange-300 transition-colors">
                  Terms of Service
                </Link>{" "}
                and{" "}
                <Link href="/privacy" className="text-orange-400 hover:text-orange-300 transition-colors">
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
