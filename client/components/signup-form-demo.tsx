"use client";
import type React from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

export default function SignupFormDemo({
  onSubmit,
  isSignUp = false,
}: {
  onSubmit: (e: React.FormEvent) => void;
  isSignUp?: boolean;
}) {
  return (
    <div className="w-full max-w-md mx-auto relative">
      {/* Clean frosted card */}
      <div
        className={cn(
          "relative rounded-2xl overflow-hidden",
          "bg-gradient-to-br from-black/40 via-black/30 to-black/25",
          "backdrop-blur-md border border-white/10 shadow-lg p-6 md:p-8"
        )}
      >
        {/* Card header */}
        <header className="mb-6 text-center">
          <h3 className="text-2xl md:text-3xl font-semibold text-white leading-tight">
            {isSignUp ? "Create an account" : "Welcome back"}
          </h3>
          <p className="mt-2 text-sm text-white/70 max-w-[36ch] mx-auto">
            {isSignUp
              ? "Create your account to start automating workflows."
              : "Sign in to your account to continue."}
          </p>
        </header>

        {/* Form */}
        <form onSubmit={onSubmit} className="space-y-5">
          {isSignUp && (
            <Field label="Full name" htmlFor="name">
              <Input
                id="name"
                name="name"
                type="text"
                placeholder="Jane Doe"
                required
                className="bg-white/10 placeholder:text-white/40 text-white rounded-md px-4 py-3 border border-white/10 focus:ring-2 focus:ring-indigo-400 focus:outline-none transition"
              />
            </Field>
          )}

          <Field label="Email address" htmlFor="email">
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="you@company.com"
              required
              className="bg-white/10 placeholder:text-white/40 text-white rounded-md px-4 py-3 border border-white/10 focus:ring-2 focus:ring-indigo-400 focus:outline-none transition"
            />
          </Field>

          <Field label="Password" htmlFor="password">
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              required
              className="bg-white/10 placeholder:text-white/40 text-white rounded-md px-4 py-3 border border-white/10 focus:ring-2 focus:ring-indigo-400 focus:outline-none transition"
            />
          </Field>

          {/* Actions row */}
          <div className="flex items-center justify-between gap-4">
            <Button
              type="submit"
              className="flex-1 h-12 rounded-md bg-white/90 text-black font-medium shadow-sm hover:bg-white transition-colors"
            >
              {isSignUp ? "Create account" : "Sign in"}
            </Button>

            {!isSignUp && (
              <button
                type="button"
                onClick={() => {
                  alert("Forgot password flow — wire your route here");
                }}
                className="text-sm text-white/70 hover:text-white transition"
              >
                Forgot?
              </button>
            )}
          </div>

          {/* Legal microcopy */}
          <p className="text-xs text-white/60 text-center mt-1">
            By continuing you agree to our{" "}
            <u className="hover:text-white cursor-pointer">Terms</u> and{" "}
            <u className="hover:text-white cursor-pointer">Privacy Policy</u>.
          </p>
        </form>
      </div>
    </div>
  );
}

/* Small helper component for consistent label + slot */
function Field({
  children,
  label,
  htmlFor,
}: {
  children: React.ReactNode;
  label: string;
  htmlFor: string;
}) {
  return (
    <label htmlFor={htmlFor} className="block">
      <span className="text-xs font-medium tracking-widest text-white/80">
        {label.toUpperCase()}
      </span>
      <div className="mt-2">{children}</div>
    </label>
  );
}
