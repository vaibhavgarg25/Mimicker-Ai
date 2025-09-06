"use client"
import type React from "react"
import { useState } from "react"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function ForgotPasswordForm() {
  const [email, setEmail] = useState("")
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle")
  const [message, setMessage] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus("loading")
    setMessage("")

    try {
      const res = await fetch("http://localhost:8000/api/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      })

      const data = await res.json()
      if (res.ok) {
        setStatus("success")
        setMessage("Reset link sent! Check your inbox.")
      } else {
        setStatus("error")
        setMessage(data.message || "Something went wrong.")
      }
    } catch (err) {
      setStatus("error")
      setMessage("Network error. Try again.")
    }
  }

  return (
    <div className="w-full max-w-md mx-auto relative">
      <div className="relative rounded-2xl overflow-hidden bg-gradient-to-br from-black/40 via-black/30 to-black/25 backdrop-blur-md border border-white/10 shadow-lg p-6 md:p-8">
        <header className="mb-6 text-center">
          <h3 className="text-2xl md:text-3xl font-semibold text-white leading-tight">
            Forgot your password?
          </h3>
          <p className="mt-2 text-sm text-white/70">
            Enter your email and we’ll send you a reset link.
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-5">
          <label htmlFor="email" className="block">
            <span className="text-xs font-medium tracking-widest text-white/80">EMAIL ADDRESS</span>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="you@company.com"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-2 bg-white/10 placeholder:text-white/40 text-white rounded-md px-4 py-3 border border-white/10 focus:ring-2 focus:ring-indigo-400 focus:outline-none transition"
            />
          </label>

          <Button
            type="submit"
            disabled={status === "loading"}
            className="w-full h-12 rounded-md bg-white/90 text-black font-medium shadow-sm hover:bg-white transition-colors"
          >
            {status === "loading" ? "Sending..." : "Send reset link"}
          </Button>

          {message && (
            <p
              className={`text-sm mt-2 ${
                status === "success" ? "text-green-400" : "text-red-400"
              }`}
            >
              {message}
            </p>
          )}
        </form>
      </div>
    </div>
  )
}
