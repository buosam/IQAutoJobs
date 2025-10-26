import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import Header from "@/components/ui/header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "IQAutoJobs - Find Your Dream Job",
  description: "Connect with top companies and discover opportunities that match your skills and aspirations. Your next career move starts here.",
  keywords: ["jobs", "careers", "employment", "recruitment", "hiring", "job search", "career opportunities", "talent acquisition"],
  authors: [{ name: "IQAutoJobs Team" }],
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  openGraph: {
    title: "IQAutoJobs - Find Your Dream Job",
    description: "Connect with top companies and discover opportunities that match your skills and aspirations.",
    url: "https://iqautojobs.com",
    siteName: "IQAutoJobs",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "IQAutoJobs - Find Your Dream Job",
    description: "Connect with top companies and discover opportunities that match your skills and aspirations.",
  },
  alternates: {
    canonical: "https://iqautojobs.com",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        <Header />
        <main>{children}</main>
        {children}
        <Toaster />
      </body>
    </html>
  );
}
