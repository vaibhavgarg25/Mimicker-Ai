"use client";

import { Navigation } from "@/components/navigation";
import SpotlightCard from "@/components/SpotlightCard";
import {
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Sparkles, Target, Users, Lightbulb } from "lucide-react";

export default function AboutPage() {
  const teamMembers = [
    {
      name: "Dilip S",
      role: "AI Engineer",
      avatar: "/team/Dilip.jpg",
      initials: "DS",
    },
    {
      name: "Prachi P",
      role: "Product Designer",
      avatar: "/team/Prachi.png",
      initials: "PP",
    },
    {
      name: "Vaibhav G",
      role: "Full Stack Developer",
      avatar: "/team/Vaibhav.jpg",
      initials: "VG",
    },
    {
      name: "Mervin",
      role: "Frontend Developer",
      avatar: "/team/Mervin.jpg",
      initials: "M",
    },
  ];

  return (
    <div
      className="min-h-screen relative"
      style={{ backgroundColor: "#050505" }}
    >
      <div className="relative z-10">
        <Navigation />

        <div className="container mx-auto px-4 py-20">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-6xl font-thin tracking-wider mb-6 text-balance text-foreground uppercase">
              Revolutionizing Web Automation
            </h1>

            <p className="text-xl font-thin tracking-wide text-foreground/70 max-w-3xl mx-auto text-balance leading-relaxed">
              We believe that automation should be accessible to everyone, not
              just developers. That's why we created Mimicker AI - to
              democratize web automation through the power of artificial
              intelligence.
            </p>
          </div>

          {/* Problem & Solution */}
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            <SpotlightCard
              className="bg-foreground/5 border-foreground/10 backdrop-blur-sm"
              spotlightColor="rgba(255, 107, 53, 0.15)"
            >
              <CardHeader>
                <div className="size-12 rounded-lg bg-red-500/10 flex items-center justify-center mb-4">
                  <Target className="size-6 text-red-400" />
                </div>
                <CardTitle className="text-2xl font-thin tracking-wide text-foreground uppercase">
                  The Problem
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-foreground/70 font-thin tracking-wide leading-relaxed">
                  Millions of people perform repetitive web tasks daily - data
                  entry, form filling, content management, and more. Traditional
                  automation tools require programming knowledge, making them
                  inaccessible to most users who need them most.
                </p>
              </CardContent>
            </SpotlightCard>

            <SpotlightCard
              className="bg-foreground/5 border-foreground/10 backdrop-blur-sm"
              spotlightColor="rgba(255, 107, 53, 0.15)"
            >
              <CardHeader>
                <div className="size-12 rounded-lg bg-orange-500/10 flex items-center justify-center mb-4">
                  <Lightbulb className="size-6 text-orange-400" />
                </div>
                <CardTitle className="text-2xl font-thin tracking-wide text-foreground uppercase">
                  Our Solution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-foreground/70 font-thin tracking-wide leading-relaxed">
                  Mimicker AI bridges this gap by allowing users to simply
                  record their actions. Our advanced AI analyzes the recording,
                  understands the workflow, and generates clean, executable
                  automation scripts that can be run anywhere.
                </p>
              </CardContent>
            </SpotlightCard>
          </div>

          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-6xl font-thin tracking-wider mb-6 text-balance text-foreground uppercase">
              MEET THE TEAM{" "}
            </h1>
          </div>
          {/* Team Section */}
          <div className="grid md:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {teamMembers.map((member, index) => (
              <SpotlightCard
                key={index}
                className="bg-foreground/5 border-foreground/10 backdrop-blur-sm text-center"
                spotlightColor="rgba(255, 107, 53, 0.15)"
              >
                <CardHeader>
                  <Avatar className="w-24 h-24 mx-auto mb-4 rounded-full overflow-hidden">
                    <AvatarImage
                      src={member.avatar}
                      alt={member.name}
                      className="object-cover w-full h-full"
                    />
                    <AvatarFallback className="text-lg font-semibold bg-foreground/10 text-foreground">
                      {member.initials}
                    </AvatarFallback>
                  </Avatar>

                  <CardTitle className="text-xl font-thin tracking-wide text-foreground uppercase">
                    {member.name}
                  </CardTitle>
                  <CardDescription className="text-orange-400 font-thin tracking-wider uppercase">
                    {member.role}
                  </CardDescription>
                </CardHeader>
              </SpotlightCard>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
