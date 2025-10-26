import { AdminNav } from "@/components/admin-nav"

// Mock admin user data - in a real app, this would come from authentication
const mockAdminUser = {
  id: "1",
  name: "Admin User",
  email: "admin@iqautojobs.com",
  role: "admin"
}

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-background">
      <AdminNav user={mockAdminUser} />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}