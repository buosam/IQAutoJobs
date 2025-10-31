
import { isValidRedirectUrl, getApiError } from '../utils';

describe('isValidRedirectUrl', () => {
  it('should return true for valid relative URLs', () => {
    expect(isValidRedirectUrl('/dashboard')).toBe(true);
    expect(isValidRedirectUrl('/profile/settings')).toBe(true);
    expect(isValidRedirectUrl('/')).toBe(true);
  });

  it.each([
    ['absolute URL', 'http://example.com'],
    ['absolute URL', 'https://example.com/path'],
    ['protocol-relative URL', '//example.com'],
    ['URL with javascript scheme', 'javascript:alert(1)'],
    ['URL with mailto scheme', 'mailto:test@example.com'],
    ['null input', null],
    ['undefined input', undefined as any],
    ['empty string', ''],
    ['URL that does not start with a forward slash', 'dashboard'],
  ])('should return false for invalid input (%s)', (_, value) => {
    expect(isValidRedirectUrl(value)).toBe(false);
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
