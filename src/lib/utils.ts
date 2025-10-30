import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function isValidRedirectUrl(url: string | null | undefined): boolean {
  if (!url) {
    return false;
  }
  // A valid redirect URL must be a relative path, but not a protocol-relative URL.
  return url.startsWith("/") && !url.startsWith("//");
}

export async function getApiError(response: Response, defaultMessage: string = "An unexpected error occurred."): Promise<string> {
  const responseText = await response.text();
  try {
    const errorData = JSON.parse(responseText);
    return errorData?.detail || errorData?.error?.message || defaultMessage;
  } catch (e) {
    console.error("Failed to parse JSON error response. Raw response:", responseText);
    return "An unexpected error occurred.";
  }
}
