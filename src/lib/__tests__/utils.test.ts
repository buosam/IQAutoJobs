import { isValidRedirectUrl } from '../utils';

describe('isValidRedirectUrl', () => {
  it('should return true for valid relative URLs', () => {
    expect(isValidRedirectUrl('/dashboard')).toBe(true);
    expect(isValidRedirectUrl('/profile/settings')).toBe(true);
    expect(isValidRedirectUrl('/')).toBe(true);
  });

  it('should return false for absolute URLs', () => {
    expect(isValidRedirectUrl('http://example.com')).toBe(false);
    expect(isValidRedirectUrl('https://example.com/path')).toBe(false);
  });

  it('should return false for protocol-relative URLs', () => {
    expect(isValidRedirectUrl('//example.com')).toBe(false);
  });

  it('should return false for URLs with invalid schemes', () => {
    expect(isValidRedirectUrl('javascript:alert(1)')).toBe(false);
    expect(isValidRedirectUrl('mailto:test@example.com')).toBe(false);
  });

  it('should return false for null, undefined, or empty strings', () => {
    expect(isValidRedirectUrl(null)).toBe(false);
    expect(isValidRedirectUrl(undefined)).toBe(false);
    expect(isValidRedirectUrl('')).toBe(false);
  });

  it('should return false for urls that do not start with a forward slash', () => {
    expect(isValidRedirectUrl('dashboard')).toBe(false);
  });
});
