import { EmployerNav } from "@/components/employer-nav"

// Mock user data - in a real app, this would come from authentication
const mockUser = {
  id: "1",
  name: "John Doe",
  email: "john.doe@company.com",
  company: {
    name: "Tech Corp",
    logo_url: "/logo.svg"
  }
}

export default function EmployerLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-background">
      <EmployerNav user={mockUser} />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}