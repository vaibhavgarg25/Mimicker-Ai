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
  const [userEmail, setUserEmail] = useState<string | null>(null)
  const [userName, setUserName] = useState<string | null>(null)

  useEffect(() => {
    const checkLoginStatus = () => {
      const token = localStorage.getItem("token")
      const email = localStorage.getItem("userEmail")
      const name= localStorage.getItem("userName")
      setIsLoggedIn(!!token)
      setUserEmail(email)
      setUserName(name)
    }

    checkLoginStatus()
    window.addEventListener("storage", checkLoginStatus)
    return () => window.removeEventListener("storage", checkLoginStatus)
  }, [])

  const handleLogout = () => {
    localStorage.clear()
    setIsLoggedIn(false)
    setUserEmail(null)
    toast.success("Logged out successfully!")
    window.location.href = "/"
  }

  const navItems = [
    { href: "/", label: "Home" },
    { href: "/about", label: "About" },
    { href: "/how-to-use", label: "How to Use" },
    { href: "/manual", label: "Manual" },
    ...(isLoggedIn
      ? [{ href: "/dashboard", label: "Dashboard" }]
      : [{ href: "/signup", label: "Sign Up / Login" }]),
  ]

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        {/* Logo */}
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
            <div className="flex items-center gap-4 ml-6">
              {/* Email as badge */}
              <span className="px-3 py-1 text-xs rounded-full bg-muted text-muted-foreground">
                {userName}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
                className="flex items-center gap-2"
              >
                <LogOut className="size-4" />
                Sign Out
              </Button>
            </div>
          )}
        </div>

        {/* Mobile Navigation */}
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
          <SheetTrigger asChild className="md:hidden">
            <Button variant="ghost" size="sm">
              <Menu className="size-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-[280px] flex flex-col justify-between">
            {/* Links */}
            <div className="flex flex-col gap-4 mt-8">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className="text-base font-medium text-muted-foreground hover:text-primary transition-colors"
                >
                  {item.label}
                </Link>
              ))}
            </div>

            {/* User Info & Logout */}
            {isLoggedIn && (
              <div className="flex flex-col gap-3 border-t pt-4">
                <span className="text-sm text-muted-foreground">{userEmail}</span>
                <Button
                  variant="outline"
                  onClick={() => {
                    handleLogout()
                    setIsOpen(false)
                  }}
                  className="flex items-center gap-2"
                >
                  <LogOut className="size-4" />
                  Sign Out
                </Button>
              </div>
            )}
          </SheetContent>
        </Sheet>
      </div>
    </nav>
  )
}
