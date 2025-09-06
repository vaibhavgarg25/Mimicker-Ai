"use client"
import type React from "react"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

export default function SignupFormDemo({
  onSubmit,
  isSignUp = false,
}: {
  onSubmit: (e: React.FormEvent) => void
  isSignUp?: boolean
}) {
  return (
    <div className="max-w-md w-full mx-auto rounded-2xl p-6 md:p-8 relative">
      <div className="absolute inset-0 bg-white/10 dark:bg-white/5 backdrop-blur-2xl rounded-2xl border border-white/20 dark:border-white/10 shadow-[0_8px_32px_0_rgba(31,38,135,0.37)]" />
      <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-transparent dark:from-white/10 dark:via-white/5 dark:to-transparent rounded-2xl" />
      <div className="absolute inset-0 bg-gradient-to-t from-black/5 via-transparent to-white/10 dark:from-white/5 dark:via-transparent dark:to-white/5 rounded-2xl" />

      <div className="relative z-10">
        <h2 className="font-bold text-xl text-gray-800 dark:text-white">{isSignUp ? "Sign Up" : "Login"}</h2>
        <p className="text-gray-600 text-sm max-w-sm mt-2 dark:text-gray-300">
          Enter your email and password to continue
        </p>

        <form className="my-8" onSubmit={onSubmit}>
          {isSignUp && (
            <LabelInputContainer className="mb-4">
              <Label htmlFor="name" className="text-gray-700 dark:text-gray-200">
                Full Name
              </Label>
              <Input
                id="name"
                name="name"
                placeholder="Tyler Durden"
                type="text"
                required
                className="bg-white/20 dark:bg-white/10 backdrop-blur-sm border-white/30 dark:border-white/20 text-gray-800 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:bg-white/30 dark:focus:bg-white/15 transition-all duration-200"
              />
            </LabelInputContainer>
          )}
          <LabelInputContainer className="mb-4">
            <Label htmlFor="email" className="text-gray-700 dark:text-gray-200">
              Email Address
            </Label>
            <Input
              id="email"
              name="email"
              placeholder="projectmayhem@fc.com"
              type="email"
              required
              className="bg-white/20 dark:bg-white/10 backdrop-blur-sm border-white/30 dark:border-white/20 text-gray-800 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:bg-white/30 dark:focus:bg-white/15 transition-all duration-200"
            />
          </LabelInputContainer>
          <LabelInputContainer className="mb-4">
            <Label htmlFor="password" className="text-gray-700 dark:text-gray-200">
              Password
            </Label>
            <Input
              id="password"
              name="password"
              placeholder="••••••••"
              type="password"
              required
              className="bg-white/20 dark:bg-white/10 backdrop-blur-sm border-white/30 dark:border-white/20 text-gray-800 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400 focus:bg-white/30 dark:focus:bg-white/15 transition-all duration-200"
            />
          </LabelInputContainer>

          <Button
            className="bg-gray-900/80 hover:bg-gray-900/90 dark:bg-white/20 dark:hover:bg-white/30 backdrop-blur-sm relative group/btn w-full text-white dark:text-white rounded-md h-10 font-medium border border-gray-700/50 dark:border-white/20 shadow-lg hover:shadow-xl transition-all duration-200"
            type="submit"
          >
            {isSignUp ? "Sign up" : "Sign in"} &rarr;
            <BottomGradient />
          </Button>
        </form>
      </div>
    </div>
  )
}

const BottomGradient = () => {
  return (
    <>
      <span className="group-hover/btn:opacity-100 block transition duration-500 opacity-0 absolute h-px w-full -bottom-px inset-x-0 bg-gradient-to-r from-transparent via-cyan-400 to-transparent" />
      <span className="group-hover/btn:opacity-100 blur-sm block transition duration-500 opacity-0 absolute h-px w-1/2 mx-auto -bottom-px inset-x-10 bg-gradient-to-r from-transparent via-indigo-400 to-transparent" />
    </>
  )
}

const LabelInputContainer = ({
  children,
  className,
}: {
  children: React.ReactNode
  className?: string
}) => {
  return <div className={cn("flex flex-col space-y-2 w-full", className)}>{children}</div>
}
