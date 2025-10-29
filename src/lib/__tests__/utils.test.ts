
import { getApiError } from '../utils';

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
