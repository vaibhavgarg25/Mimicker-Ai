"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "sonner";
import { ArrowLeft } from "lucide-react";
import SignupFormDemo from "@/components/signup-form-demo";
import Link from "next/link";
import PrismaticBurst from "@/components/PrismaticBurst/PrismaticBurst";

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState("signin");
  const router = useRouter();

  // Base URL of your Flask backend
  const API_URL = "http://localhost:8000/api/auth";

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || "Login failed");
      }

      const data = await res.json();
      // Save token/user info
      localStorage.setItem("isLoggedIn", "true");
      localStorage.setItem("userEmail", data.data.user.email);
      localStorage.setItem("userName", data.data.user.name);
      localStorage.setItem("token", data.data.token);

      // inform other windows
      window.dispatchEvent(new Event("storage"));

      toast.success("Successfully signed in!");
      router.push("/dashboard");
    } catch (err: any) {
      toast.error(err.message || "Error signing in");
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const name = formData.get("name") as string;
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    try {
      const res = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || "Signup failed");
      }

      const data = await res.json();

      // Save token/user info
      localStorage.setItem("isLoggedIn", "true");
      localStorage.setItem("userEmail", email);
      localStorage.setItem("userName", name);
      localStorage.setItem("token", data.token);

      window.dispatchEvent(new Event("storage"));

      toast.success("Account created successfully!");
      router.push("/dashboard");
    } catch (err: any) {
      toast.error(err.message || "Error creating account");
    }
  };

  return (
    <div className="min-h-screen relative bg-black overflow-hidden text-gray-50">
      {/* Prismatic background - full bleed behind content */}
      <div className="absolute inset-0">
        <div style={{ width: "100%", height: "100%", position: "relative" }}>
          <PrismaticBurst
            animationType="hover"
            intensity={2}
            speed={0.5}
            distort={2.6}
            paused={false}
            offset={{ x: 0, y: 0 }}
            hoverDampness={0.25}
            rayCount={24}
            mixBlendMode="lighten"
            colors={["#ff007a", "#4d3dff", "#ffffff"]}
          />
          {/* subtle overlay so text is legible */}
          <div className="absolute inset-0 bg-black/40" />
        </div>
      </div>

      {/* Back to Home - simplified (no glass/backdrop-blur) */}
      <div className="absolute top-6 left-6 z-30">
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-black/70 border border-white/10 text-white hover:bg-black/80 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>
      </div>

      {/* CONTENT: centered vertically and spaced out horizontally */}
      <div className="relative z-10">
        <div className="max-w-7xl mx-auto px-6 py-0">
          {/* full viewport height so centering is exact; larger horizontal gap */
          /* items-center vertically centers both columns */}
          <div className="grid grid-cols-12 gap-x-16 items-center min-h-screen">
            {/* LEFT: heading + subtext only (uses your specified styles) */}
            <div className="col-span-12 lg:col-span-7">
              <div className="flex items-center h-full">
                <div>
                  {/* Foreground layout */}
                  <div className="relative z-10 flex flex-col items-start justify-center h-full px-0 text-left">
                    <h1
                      className="text-[64px] md:text-[120px] leading-none font-thin tracking-[8px] text-white/95 select-none"
                      style={{
                        letterSpacing: "1.8rem",
                        WebkitTextStroke: "0.5px rgba(255,255,255,0.02)",
                      }}
                    >
                      MIMICKER
                    </h1>

                    <div className="w-36 h-[1px] bg-white/20 my-6" />

                    <p className="max-w-2xl text-sm md:text-base text-white/60 mb-6 px-0">
                      Automate web tasks by showing — not coding. Upload a screen
                      recording, and let the AI create a clean JSON automation script.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* RIGHT: glassmorphism card containing tabs & form (kept as-is) */}
            <div className="col-span-12 lg:col-span-5 flex items-center justify-center">
              <div className="w-full max-w-md relative rounded-3xl p-1">
                {/* Glass background */}
                <div className="backdrop-blur-xl bg-white/6 border border-white/10 rounded-3xl shadow-2xl p-8 relative z-20">
                  
                  

                  <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                    <TabsList className="grid w-full grid-cols-2 mb-6 bg-white/3 rounded-lg p-1">
                      <TabsTrigger
                        value="signin"
                        className="data-[state=active]:bg-white/30 text-white/90 data-[state=active]:text-black"
                      >
                        Sign In
                      </TabsTrigger>
                      <TabsTrigger
                        value="signup"
                        className="data-[state=active]:bg-white/30 text-white/90 data-[state=active]:text-black"
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

                  <div className="text-center mt-4">
                    <p className="text-xs text-white/60">
                      By continuing, you agree to our{" "}
                      <Link href="/terms" className="underline text-white/90">
                        Terms
                      </Link>{" "}
                      and{" "}
                      <Link href="/privacy" className="underline text-white/90">
                        Privacy Policy
                      </Link>
                    </p>
                  </div>
                </div>

                {/* Decorative outer glow to emphasize glass */}
                <div
                  className="absolute -inset-px rounded-3xl bg-gradient-to-r from-white/5 via-transparent to-white/3 pointer-events-none"
                  style={{ filter: "blur(18px)" }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
