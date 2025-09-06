import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Sparkles, Target, Users, Lightbulb } from "lucide-react"

export default function AboutPage() {
  const teamMembers = [
    {
      name: "Alex Chen",
      role: "AI Engineer",
      avatar: "/professional-asian-male-headshot.png",
      initials: "AC",
    },
    {
      name: "Sarah Johnson",
      role: "Product Designer",
      avatar: "/professional-headshot-female.png",
      initials: "SJ",
    },
    {
      name: "Mike Rodriguez",
      role: "Full Stack Developer",
      avatar: "/professional-headshot-hispanic-male.jpg",
      initials: "MR",
    },
  ]

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navigation />

      <div className="container mx-auto px-4 py-20">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-8">
            <Sparkles className="size-4 text-primary" />
            <span className="text-sm font-medium text-primary">About Mimicker AI</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-bold mb-6 text-balance">Revolutionizing Web Automation</h1>

          <p className="text-xl text-muted-foreground max-w-3xl mx-auto text-balance">
            We believe that automation should be accessible to everyone, not just developers. That's why we created
            Mimicker AI - to democratize web automation through the power of artificial intelligence.
          </p>
        </div>

        {/* Problem & Solution */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <Card className="border-primary/20">
            <CardHeader>
              <div className="size-12 rounded-lg bg-destructive/10 flex items-center justify-center mb-4">
                <Target className="size-6 text-destructive" />
              </div>
              <CardTitle className="text-2xl">The Problem</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed">
                Millions of people perform repetitive web tasks daily - data entry, form filling, content management,
                and more. Traditional automation tools require programming knowledge, making them inaccessible to most
                users who need them most.
              </p>
            </CardContent>
          </Card>

          <Card className="border-primary/20">
            <CardHeader>
              <div className="size-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Lightbulb className="size-6 text-primary" />
              </div>
              <CardTitle className="text-2xl">Our Solution</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed">
                Mimicker AI bridges this gap by allowing users to simply record their actions. Our advanced AI analyzes
                the recording, understands the workflow, and generates clean, executable automation scripts that can be
                run anywhere.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Team Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-8">
            <Users className="size-4 text-primary" />
            <span className="text-sm font-medium text-primary">Meet the Team</span>
          </div>

          <h2 className="text-3xl md:text-4xl font-bold mb-6">Built by Automation Enthusiasts</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Our diverse team combines expertise in AI, design, and development to create the most intuitive automation
            platform.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {teamMembers.map((member, index) => (
            <Card
              key={index}
              className="border-primary/20 text-center hover:border-primary/40 transition-all duration-300"
            >
              <CardHeader>
                <Avatar className="size-20 mx-auto mb-4">
                  <AvatarImage src={member.avatar || "/placeholder.svg"} alt={member.name} />
                  <AvatarFallback className="text-lg font-semibold bg-primary/10 text-primary">
                    {member.initials}
                  </AvatarFallback>
                </Avatar>
                <CardTitle className="text-xl">{member.name}</CardTitle>
                <CardDescription className="text-primary font-medium">{member.role}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
