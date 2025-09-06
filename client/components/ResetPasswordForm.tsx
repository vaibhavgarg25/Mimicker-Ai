"use client"
import type React from "react"
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function ResetPasswordForm({ token }: { token: string }) {
  const [password, setPassword] = useState("")
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle")
  const [message, setMessage] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus("loading")
    setMessage("")

    try {
      const res = await fetch("http://localhost:8000/api/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, password }),
      })

      const data = await res.json()
      if (res.ok) {
        setStatus("success")
        setMessage("Password reset successful! You can now log in.")
      } else {
        setStatus("error")
        setMessage(data.message || "Something went wrong.")
      }
    } catch {
      setStatus("error")
      setMessage("Network error. Try again.")
    }
  }

  return (
    <div className="w-full max-w-md mx-auto relative">
      <div className="relative rounded-2xl overflow-hidden bg-gradient-to-br from-black/40 via-black/30 to-black/25 backdrop-blur-md border border-white/10 shadow-lg p-6 md:p-8">
        <header className="mb-6 text-center">
          <h3 className="text-2xl md:text-3xl font-semibold text-white leading-tight">
            Reset your password
          </h3>
          <p className="mt-2 text-sm text-white/70">Choose a new password below.</p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-5">
          <label htmlFor="password" className="block">
            <span className="text-xs font-medium tracking-widest text-white/80">NEW PASSWORD</span>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-2 bg-white/10 placeholder:text-white/40 text-white rounded-md px-4 py-3 border border-white/10 focus:ring-2 focus:ring-indigo-400 focus:outline-none transition"
            />
          </label>

          <Button
            type="submit"
            disabled={status === "loading"}
            className="w-full h-12 rounded-md bg-white/90 text-black font-medium shadow-sm hover:bg-white transition-colors"
          >
            {status === "loading" ? "Resetting..." : "Reset password"}
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
