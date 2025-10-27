import { isValidRedirectUrl } from "../utils"

describe("isValidRedirectUrl", () => {
  it("should return true for valid relative URLs", () => {
    expect(isValidRedirectUrl("/dashboard")).toBe(true)
    expect(isValidRedirectUrl("/profile/settings")).toBe(true)
  })

  it("should return false for absolute URLs", () => {
    expect(isValidRedirectUrl("https://google.com")).toBe(false)
    expect(isValidRedirectUrl("http://evil-site.com")).toBe(false)
  })

  it("should return false for protocol-relative URLs", () => {
    expect(isValidRedirectUrl("//google.com")).toBe(false)
  })

  it("should return false for URLs that are not relative paths", () => {
    expect(isValidRedirectUrl("dashboard")).toBe(false)
  })

  it("should return false for null or empty strings", () => {
    expect(isValidRedirectUrl(null)).toBe(false)
    expect(isValidRedirectUrl("")).toBe(false)
  })
})
