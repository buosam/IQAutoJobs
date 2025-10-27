import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function isValidRedirectUrl(url: string | null): boolean {
  if (!url) {
    return false;
  }
  // A valid redirect URL must be a relative path, but not a protocol-relative URL.
  return url.startsWith("/") && !url.startsWith("//");
}
