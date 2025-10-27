import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import LoginForm from '../LoginForm';
import { useRouter, useSearchParams } from 'next/navigation';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
  useSearchParams: jest.fn(),
}));

describe('LoginForm', () => {
  const mockRouter = {
    push: jest.fn(),
  };

  beforeEach(() => {
    (useRouter as jest.Mock).mockReturnValue(mockRouter);
    (useSearchParams as jest.Mock).mockReturnValue(new URLSearchParams());
    Object.defineProperty(window, 'location', {
      writable: true,
      value: { href: '' },
    });
  });

  it('should not include an invalid returnTo parameter in the Google login URL', () => {
    (useSearchParams as jest.Mock).mockReturnValue(new URLSearchParams('returnTo=http://malicious.com'));
    render(<LoginForm />);
    fireEvent.click(screen.getByText('Continue with Google'));
    expect(window.location.href).toBe('/api/oauth/google/login?');
  });

  it('should include a valid returnTo parameter in the Google login URL', () => {
    (useSearchParams as jest.Mock).mockReturnValue(new URLSearchParams('returnTo=/dashboard'));
    render(<LoginForm />);
    fireEvent.click(screen.getByText('Continue with Google'));
    expect(window.location.href).toBe('/api/oauth/google/login?returnTo=%2Fdashboard');
  });
});
