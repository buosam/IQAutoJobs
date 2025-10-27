import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function isValidRedirectUrl(url: string | null): boolean {
  if (!url) return false
  // Disallow absolute URLs and protocol-relative URLs
  if (url.startsWith("http:") || url.startsWith("https:") || url.startsWith("//")) {
    return false
  }
  // Ensure it's a relative path
  return url.startsWith("/")
}
