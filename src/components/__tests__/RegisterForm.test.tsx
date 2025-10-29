import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import RegisterForm from '../auth/RegisterForm';
import { PAGE_ROUTES } from '@/lib/constants';

const mockPush = jest.fn();
const mockGet = jest.fn();

jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
  useSearchParams: () => ({
    get: mockGet,
  }),
}));

global.fetch = jest.fn();

async function fillAndSubmitForm() {
  fireEvent.change(screen.getByLabelText(/First Name/i), { target: { value: 'Test' } });
  fireEvent.change(screen.getByLabelText(/Last Name/i), { target: { value: 'User' } });
  fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
  fireEvent.change(screen.getByLabelText(/^Password/i), { target: { value: 'password123' } });
  fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'password123' } });
  fireEvent.click(screen.getByText('Create Account'));
}

describe('RegisterForm', () => {
  const originalLocation = window.location;

  beforeAll(() => {
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: { href: '' },
    });
  });

  afterAll(() => {
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: originalLocation,
    });
  });

  beforeEach(() => {
    jest.clearAllMocks();
    (fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ user: { first_name: 'Test', role: 'CANDIDATE' } }),
    });
  });

  it('redirects to a valid returnTo URL after successful registration', async () => {
    mockGet.mockImplementation((param: string) => {
      if (param === 'returnTo') {
        return '/test-redirect';
      }
      return null;
    });

    render(<RegisterForm />);
    await fillAndSubmitForm();

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/test-redirect');
    });
  });

  it('redirects to the dashboard when returnTo URL is invalid', async () => {
    mockGet.mockImplementation((param: string) => {
      if (param === 'returnTo') {
        return 'http://malicious.com';
      }
      return null;
    });

    render(<RegisterForm />);
    await fillAndSubmitForm();

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith(PAGE_ROUTES.DASHBOARD);
    });
  });

  it('correctly handles the returnTo parameter for Google signups', () => {
    mockGet.mockImplementation((param: string) => {
      if (param === 'returnTo') {
        return 'http://malicious.com';
      }
      return null;
    });

    render(<RegisterForm />);
    fireEvent.click(screen.getByText('Sign up with Google'));

    expect(window.location.href).toBe('/api/oauth/google/login?');
  });
});
