import { CandidateNav } from "@/components/candidate-nav"

// Mock user data - in a real app, this would come from authentication
const mockUser = {
  id: "1",
  name: "Jane Smith",
  email: "jane.smith@email.com",
  avatar_url: "/logo.svg"
}

export default function CandidateLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-background">
      <CandidateNav user={mockUser} />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}