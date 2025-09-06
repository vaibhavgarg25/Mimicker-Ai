"use client"

import type React from "react"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { toast } from "sonner"
import { User, Mail, Lock } from "lucide-react"

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState("signin")
  const router = useRouter()

  // Base URL of your Flask backend
  const API_URL = "http://localhost:8000/api/auth"

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    const email = formData.get("email") as string
    const name=formData.get("name") as string
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
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />

      <div className="container mx-auto px-4 py-20">
        <div className="max-w-md mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">Welcome to Mimicker AI</h1>
            <p className="text-muted-foreground">
              Sign in to access your dashboard and manage automation scripts
            </p>
          </div>

          <Card className="border-primary/20">
            <CardContent className="p-6">
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList className="grid w-full grid-cols-2 mb-6">
                  <TabsTrigger value="signin">Sign In</TabsTrigger>
                  <TabsTrigger value="signup">Sign Up</TabsTrigger>
                </TabsList>

                {/* --- Sign In --- */}
                <TabsContent value="signin">
                  <form onSubmit={handleSignIn} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="signin-email">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 size-4 text-muted-foreground" />
                        <Input
                          id="signin-email"
                          name="email"
                          type="email"
                          placeholder="Enter your email"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="signin-password">Password</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 size-4 text-muted-foreground" />
                        <Input
                          id="signin-password"
                          name="password"
                          type="password"
                          placeholder="Enter your password"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    <Button type="submit" className="w-full">
                      Sign In
                    </Button>
                  </form>
                </TabsContent>

                {/* --- Sign Up --- */}
                <TabsContent value="signup">
                  <form onSubmit={handleSignUp} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="signup-name">Full Name</Label>
                      <div className="relative">
                        <User className="absolute left-3 top-3 size-4 text-muted-foreground" />
                        <Input
                          id="signup-name"
                          name="name"
                          type="text"
                          placeholder="Enter your full name"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="signup-email">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 size-4 text-muted-foreground" />
                        <Input
                          id="signup-email"
                          name="email"
                          type="email"
                          placeholder="Enter your email"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="signup-password">Password</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 size-4 text-muted-foreground" />
                        <Input
                          id="signup-password"
                          name="password"
                          type="password"
                          placeholder="Create a password"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    <Button type="submit" className="w-full">
                      Create Account
                    </Button>
                  </form>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
