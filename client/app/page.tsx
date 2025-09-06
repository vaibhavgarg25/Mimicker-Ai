"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Navigation } from "@/components/navigation";
import { toast } from "sonner";
import { ArrowRight, Code, Globe, Brain, Shield } from "lucide-react";
import { Plasma } from "@/components/Plasma/plasma";
import  SpotlightCard  from "@/components/SpotlightCard";

type ProcessingStep = "upload" | "analyzing" | "generating" | "complete";

export default function MimickerAI() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<ProcessingStep>("upload");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [generatedScript, setGeneratedScript] = useState("");
  const [copied, setCopied] = useState(false);

  const handleGetStarted = () => {
    const userLoggedIn = localStorage.getItem("token");
    if (userLoggedIn) {
      router.push("/dashboard");
    } else {
      router.push("/signup");
    }
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      toast.success("Video uploaded successfully!");
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "video/*": [".mp4", ".mov", ".avi", ".mkv"],
    },
    maxFiles: 1,
  });

  const processVideo = async () => {
    if (!uploadedFile) return;
    setCurrentStep("analyzing");

    setTimeout(() => setCurrentStep("generating"), 2000);
    setTimeout(() => {
      setCurrentStep("complete");
      setGeneratedScript(
        `{ "name": "Web Automation Script", "version": "1.0.0", "steps": [...] }`
      );
      toast.success("Automation script generated!");
    }, 4000);
  };

  const copyScript = () => {
    navigator.clipboard.writeText(generatedScript);
    setCopied(true);
    toast.success("Script copied to clipboard!");
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadScript = () => {
    const blob = new Blob([generatedScript], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "automation-script.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success("Script downloaded!");
  };

  return (
    <div className="min-h-screen bg-[#050505] text-foreground">
      <Navigation />

      {/* ================= HERO ================= */}
      <section className="relative w-full h-[720px] md:h-screen overflow-hidden">
        {/* Plasma background */}
        <div className="absolute inset-0 -z-20">
          <Plasma
            color="#ff6b35"
            speed={0.6}
            direction="forward"
            scale={1.1}
            opacity={0.8}
            mouseInteractive={true}
          />
        </div>

        {/* Foreground layout */}
        <div className="relative z-10 flex flex-col items-center justify-center h-full px-6 text-center">
          <h1
            className="text-[92px] md:text-[120px] leading-none font-thin tracking-[24px] text-foreground/95 select-none"
            style={{
              letterSpacing: "1.8rem",
              WebkitTextStroke: "0.5px rgba(255,255,255,0.02)",
            }}
          >
            MIMICKER
          </h1>

          <div className="w-36 h-[1px] bg-foreground/20 my-6" />

          <p className="max-w-2xl text-sm md:text-base text-foreground/60 mb-10">
            Automate web tasks by showing — not coding. Upload a screen
            recording, and let the AI create a clean JSON automation script.
          </p>

          <div className="flex gap-4 items-center">
            <button
              onClick={handleGetStarted}
              className="px-8 py-3 rounded-full border border-foreground/40 text-sm md:text-base tracking-wide hover:scale-[1.02] transition-transform duration-200 backdrop-blur-sm bg-black/20"
            >
              SHOW TO AUTOMATE
            </button>

            <button
              onClick={() =>
                document
                  .getElementById("features")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
              className="px-4 py-2 rounded-full text-sm md:text-base text-foreground/60 hover:text-foreground transition-colors"
            >
              How it works
            </button>
          </div>
        </div>

        <div className="absolute bottom-6 right-6 z-20 text-[11px] text-foreground/40 tracking-wider">
          NODE: ACTIVATION COMPLETE, ENERGY CONVERGING
        </div>
      </section>

      {/* ================= Features ================= */}
      <section id="features" className="py-20 px-4 bg-muted/20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Choose Mimicker AI?
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Transform your manual workflows into automated scripts with the
              power of AI
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: Code,
                title: "No Coding Required",
                description:
                  "Simply record your actions and let AI generate the automation script for you",
              },
              {
                icon: Globe,
                title: "Works Anywhere",
                description:
                  "Compatible with any website or web application you can interact with",
              },
              {
                icon: Brain,
                title: "Smart AI Analysis",
                description:
                  "Advanced computer vision and NLP to understand your actions perfectly",
              },
              {
                icon: Shield,
                title: "JSON Scripts",
                description:
                  "Clean, readable JSON output that's easy to modify and integrate",
              },
            ].map((feature, index) => (
              <SpotlightCard
                key={index}
                className="hover:scale-105 transition-all duration-300"
                spotlightColor="rgba(0, 229, 255, 0.2)"
              >
                <CardHeader className="text-center">
                  <div className="size-12 rounded-lg bg-primary/10 flex items-center justify-center mx-auto mb-4">
                    <feature.icon className="size-6 text-primary" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-center">
                    {feature.description}
                  </p>
                </CardContent>
              </SpotlightCard>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-to-br from-primary/10 via-background to-accent/5 rounded-2xl p-12 border border-primary/20">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Ready to Automate Your Workflow?
            </h2>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Join thousands of users who have already automated their
              repetitive tasks with Mimicker AI
            </p>
            <Button
              size="lg"
              className="animate-pulse-glow hover:scale-105 transition-transform duration-200"
              onClick={() => {
                const userLoggedIn = localStorage.getItem("token");
                if (userLoggedIn) {
                  router.push("/dashboard");
                } else {
                  router.push("/signup");
                }
              }}
            >
              Sign Up to Get Started
              <ArrowRight className="ml-2 size-4" />
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
