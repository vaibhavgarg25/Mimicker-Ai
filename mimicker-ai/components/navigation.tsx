"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Menu, Sparkles, LogOut } from "lucide-react"
import { toast } from "sonner"

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    const checkLoginStatus = () => {
      const loginStatus = localStorage.getItem("isLoggedIn")
      setIsLoggedIn(loginStatus === "true")
    }

    checkLoginStatus()

    // Listen for storage changes to update navbar when login status changes
    window.addEventListener("storage", checkLoginStatus)

    return () => {
      window.removeEventListener("storage", checkLoginStatus)
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn")
    localStorage.removeItem("userEmail")
    setIsLoggedIn(false)
    toast.success("Logged out successfully!")
    window.location.href = "/"
  }

  const navItems = [
    { href: "/", label: "Home" },
    { href: "/about", label: "About" },
    { href: "/how-to-use", label: "How to Use" },
    { href: "/manual", label: "Manual" },
    ...(isLoggedIn ? [{ href: "/dashboard", label: "Dashboard" }] : [{ href: "/profile", label: "Sign Up/Login" }]),
  ]

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2 font-bold text-xl">
          <div className="size-8 rounded-lg bg-primary flex items-center justify-center">
            <Sparkles className="size-4 text-primary-foreground" />
          </div>
          Mimicker AI
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-6">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
            >
              {item.label}
            </Link>
          ))}
          {isLoggedIn && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
              className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
            >
              <LogOut className="size-4 mr-2" />
              Sign Out
            </Button>
          )}
        </div>

        {/* Mobile Navigation */}
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
          <SheetTrigger asChild className="md:hidden">
            <Button variant="ghost" size="sm">
              <Menu className="size-4" />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-[300px]">
            <div className="flex flex-col gap-4 mt-8">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="text-lg font-medium text-muted-foreground hover:text-primary transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {item.label}
                </Link>
              ))}
              {isLoggedIn && (
                <Button
                  variant="ghost"
                  onClick={() => {
                    handleLogout()
                    setIsOpen(false)
                  }}
                  className="text-lg font-medium text-muted-foreground hover:text-primary transition-colors justify-start p-0"
                >
                  <LogOut className="size-4 mr-2" />
                  Sign Out
                </Button>
              )}
            </div>
          </SheetContent>
        </Sheet>
      </div>
    </nav>
  )
}
