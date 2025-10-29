
import { isValidRedirectUrl, getApiError } from '../utils';

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

describe('getApiError', () => {
  it('should return the detail message from a JSON response', async () => {
    const mockResponse = new Response(JSON.stringify({ detail: 'This is a detail error' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
    const errorMessage = await getApiError(mockResponse);
    expect(errorMessage).toBe('This is a detail error');
  });

  it('should return the error message from a JSON response', async () => {
    const mockResponse = new Response(JSON.stringify({ error: { message: 'This is an error message' } }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
    const errorMessage = await getApiError(mockResponse);
    expect(errorMessage).toBe('This is an error message');
  });

  it('should return the default message if the JSON response has no known error format', async () => {
    const mockResponse = new Response(JSON.stringify({ something: 'else' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
    const errorMessage = await getApiError(mockResponse, 'Default error');
    expect(errorMessage).toBe('Default error');
  });

  it('should return the "unexpected error" message if the response is not JSON', async () => {
    const mockResponse = new Response('This is not JSON', {
      status: 500,
    });
    const errorMessage = await getApiError(mockResponse);
    expect(errorMessage).toBe('An unexpected error occurred.');
  });

  it('should return the "unexpected error" message if the response is empty', async () => {
    const mockResponse = new Response(null, {
      status: 500,
    });
    const errorMessage = await getApiError(mockResponse);
    expect(errorMessage).toBe('An unexpected error occurred.');
  });
});
