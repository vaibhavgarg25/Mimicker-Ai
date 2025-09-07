import { Navigation } from "@/components/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { VideoIcon, Eye, MessageSquare, FileCode, Play } from "lucide-react";
import { CodeBlock } from "@/components/ui/code-block";
import { Meteors } from "@/components/ui/meteors";

export default function ManualPage() {
  const technicalFlow = [
    {
      step: "Video Input",
      icon: VideoIcon,
      description: "User uploads screen recording",
      technical: "Video preprocessing, frame extraction, quality optimization",
    },
    {
      step: "Computer Vision",
      icon: Eye,
      description: "AI analyzes visual elements",
      technical:
        "Object detection, UI element recognition, OCR for text extraction",
    },
    {
      step: "Natural Language Processing",
      icon: MessageSquare,
      description: "Understanding user intent",
      technical:
        "Action classification, workflow pattern recognition, context analysis",
    },
    {
      step: "Script Generation",
      icon: FileCode,
      description: "JSON automation script creation",
      technical:
        "Selenium-compatible selectors, action sequencing, error handling",
    },
    {
      step: "Execution Ready",
      icon: Play,
      description: "Ready-to-run automation",
      technical:
        "Cross-browser compatibility, timing optimization, validation checks",
    },
  ];

  const sampleScript = `{
  "name": "Login Automation",
  "version": "1.0.0",
  "metadata": {
    "created": "2024-01-15T10:30:00Z",
    "target_url": "https://example.com/login",
    "estimated_duration": "5000ms"
  },
  "steps": [
    {
      "id": 1,
      "action": "navigate",
      "url": "https://example.com/login",
      "wait": 2000,
      "description": "Navigate to login page"
    },
    {
      "id": 2,
      "action": "wait_for_element",
      "selector": "#email-input",
      "timeout": 5000,
      "description": "Wait for email field to be visible"
    },
    {
      "id": 3,
      "action": "type",
      "selector": "#email-input",
      "text": "{{EMAIL}}",
      "clear_first": true,
      "description": "Enter email address"
    },
    {
      "id": 4,
      "action": "type",
      "selector": "#password-input",
      "text": "{{PASSWORD}}",
      "clear_first": true,
      "description": "Enter password"
    },
    {
      "id": 5,
      "action": "click",
      "selector": "button[type='submit']",
      "wait_after": 3000,
      "description": "Click login button and wait"
    },
    {
      "id": 6,
      "action": "verify",
      "selector": ".dashboard-header",
      "expected": "visible",
      "description": "Verify successful login"
    }
  ],
  "variables": {
    "EMAIL": "user@example.com",
    "PASSWORD": "secure_password"
  },
  "error_handling": {
    "retry_attempts": 3,
    "timeout_action": "screenshot_and_exit",
    "fallback_selectors": true
  }
}`;

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />

      <div className="container mx-auto px-4 py-20">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-thin tracking-wider mb-6 text-balance text-foreground uppercase">
            Technical Manual
          </h1>
          <p className="text-xl font-thin tracking-wide text-foreground/70 max-w-3xl mx-auto text-balance leading-relaxed">
            Deep dive into how Mimicker AI transforms your screen recordings
            into intelligent automation scripts
          </p>
        </div>

        {/* Technical Flow */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12">
            How It Works Under the Hood
          </h2>

          <div className="max-w-4xl mx-auto">
            {technicalFlow.map((item, index) => (
              <div key={index} className="flex gap-6 mb-8 last:mb-0">
                <div className="flex-shrink-0 flex flex-col items-center">
                  <div className="size-16 rounded-full bg-primary flex items-center justify-center mb-4">
                    <item.icon className="size-8 text-primary-foreground" />
                  </div>
                  {index < technicalFlow.length - 1 && (
                    <div className="w-px h-16 bg-border" />
                  )}
                </div>

                <Card className="flex-1 border-primary/20">
                  <CardHeader>
                    <div className="flex items-center gap-3 mb-2">
                      <Badge variant="secondary">{index + 1}</Badge>
                      <CardTitle className="text-xl">{item.step}</CardTitle>
                    </div>
                    <CardDescription className="text-lg">
                      {item.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground font-mono text-sm bg-muted/50 p-3 rounded">
                      {item.technical}
                    </p>
                  </CardContent>
                </Card>
              </div>
            ))}
          </div>
        </div>

        {/* Sample Script */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12">
            Sample JSON Script Output
          </h2>

          <Card className="max-w-4xl mx-auto border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileCode className="size-5 text-primary" />
                automation-script.json
              </CardTitle>
              <CardDescription>
                Example of a generated automation script for a login workflow
              </CardDescription>
            </CardHeader>
            <CardContent>
              <CodeBlock
                code={sampleScript}
                language="json"
                filename="automation-script.json"
              />
            </CardContent>
          </Card>
        </div>

        {/* Key Features */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12">
            Script Features
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {[
              {
                title: "Smart Selectors",
                description:
                  "Robust CSS and XPath selectors with fallback options for reliability",
              },
              {
                title: "Variable Support",
                description:
                  "Parameterized scripts with placeholder variables for reusability",
              },
              {
                title: "Error Handling",
                description:
                  "Built-in retry logic and graceful failure handling",
              },
              {
                title: "Timing Control",
                description:
                  "Intelligent wait conditions and timing optimization",
              },
              {
                title: "Cross-Browser",
                description:
                  "Compatible with Chrome, Firefox, Safari, and Edge",
              },
              {
                title: "Framework Agnostic",
                description:
                  "Works with Selenium, Puppeteer, Playwright, and more",
              },
            ].map((feature, index) => (
              <Card
                key={index}
                className="border-primary/20 hover:border-primary/40 transition-colors"
              >
                <CardHeader>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Integration Guide */}
        <Card className="max-w-4xl mx-auto border-primary/20 bg-gradient-to-br from-primary/5 to-accent/5">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Ready to Integrate?</CardTitle>
            <CardDescription className="text-lg">
              Start using Mimicker AI scripts in your automation workflow
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Badge variant="outline" className="text-sm py-2 px-4">
                pip install selenium
              </Badge>
              <Badge variant="outline" className="text-sm py-2 px-4">
                npm install puppeteer
              </Badge>
              <Badge variant="outline" className="text-sm py-2 px-4">
                npm install playwright
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
