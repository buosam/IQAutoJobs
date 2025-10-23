import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Job Board',
  description: 'Find your dream job',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body>{children}</body>
    </html>
  )
}
