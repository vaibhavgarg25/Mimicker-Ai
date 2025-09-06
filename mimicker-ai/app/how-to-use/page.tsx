import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Button } from "@/components/ui/button"
import { VideoIcon, Upload, Brain, Download, HelpCircle, ArrowRight } from "lucide-react"

export default function HowToUsePage() {
  const steps = [
    {
      icon: VideoIcon,
      title: "Record Your Task",
      description:
        "Use any screen recording software to capture yourself performing the web task you want to automate.",
      details:
        "Record at least 30 seconds of clear actions. Make sure to include all clicks, typing, and navigation steps.",
    },
    {
      icon: Upload,
      title: "Upload Your Video",
      description: "Drag and drop your recording into Mimicker AI or click to select your file.",
      details: "Supports .mp4, .mov, .avi, and .mkv formats. Maximum file size is 100MB for optimal processing.",
    },
    {
      icon: Brain,
      title: "AI Analyzes",
      description: "Our advanced AI processes your video, identifying actions, elements, and workflow patterns.",
      details: "The AI uses computer vision to detect UI elements and NLP to understand the context of your actions.",
    },
    {
      icon: Download,
      title: "Download & Run",
      description: "Get your automation script in clean JSON format, ready to run with any automation tool.",
      details: "The script includes selectors, actions, and timing information for reliable automation execution.",
    },
  ]

  const faqs = [
    {
      question: "What video formats are supported?",
      answer:
        "Mimicker AI supports .mp4, .mov, .avi, and .mkv video formats. We recommend using .mp4 for the best compatibility and processing speed.",
    },
    {
      question: "How long should my recording be?",
      answer:
        "Recordings should be at least 30 seconds and no longer than 10 minutes. This ensures we capture enough context while maintaining processing efficiency.",
    },
    {
      question: "Can I automate any website?",
      answer:
        "Yes! Mimicker AI works with any website or web application. However, sites with heavy JavaScript or dynamic content may require additional configuration.",
    },
    {
      question: "Is my data secure?",
      answer:
        "Absolutely. All videos are processed securely and deleted after script generation. We never store your personal data or sensitive information.",
    },
    {
      question: "What automation tools can run the scripts?",
      answer:
        "Our JSON scripts are compatible with Selenium, Puppeteer, Playwright, and most modern web automation frameworks.",
    },
  ]

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />

      <div className="container mx-auto px-4 py-20">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 text-balance">How to Use Mimicker AI</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto text-balance">
            Follow these simple steps to transform your manual web tasks into automated scripts
          </p>
        </div>

        {/* Steps */}
        <div className="max-w-4xl mx-auto mb-16">
          <div className="grid gap-8">
            {steps.map((step, index) => (
              <div key={index} className="flex gap-6 items-start">
                <div className="flex-shrink-0">
                  <div className="size-16 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold text-xl">
                    {index + 1}
                  </div>
                </div>

                <Card className="flex-1 border-primary/20">
                  <CardHeader>
                    <div className="flex items-center gap-3 mb-2">
                      <step.icon className="size-6 text-primary" />
                      <CardTitle className="text-2xl">{step.title}</CardTitle>
                    </div>
                    <CardDescription className="text-lg">{step.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">{step.details}</p>
                  </CardContent>
                </Card>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mb-16">
          <Card className="max-w-2xl mx-auto border-primary/20 bg-gradient-to-br from-primary/5 to-accent/5">
            <CardHeader>
              <CardTitle className="text-2xl">Ready to Get Started?</CardTitle>
              <CardDescription className="text-lg">
                Try Mimicker AI now and see how easy automation can be
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button size="lg" className="animate-pulse-glow" asChild>
                <a href="/">
                  Start Automating
                  <ArrowRight className="ml-2 size-4" />
                </a>
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* FAQ */}
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
              <HelpCircle className="size-4 text-primary" />
              <span className="text-sm font-medium text-primary">Frequently Asked Questions</span>
            </div>
            <h2 className="text-3xl md:text-4xl font-bold">Got Questions?</h2>
          </div>

          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem key={index} value={`item-${index}`} className="border border-primary/20 rounded-lg px-6">
                <AccordionTrigger className="text-left font-semibold hover:text-primary">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground leading-relaxed">{faq.answer}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </div>
  )
}
