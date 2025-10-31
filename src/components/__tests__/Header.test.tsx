import { render, screen } from '@testing-library/react';
import Header from '../ui/header';

// Mock useRouter
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      back: jest.fn(),
      forward: jest.fn(),
      prefetch: jest.fn(() => Promise.resolve()),
      refresh: jest.fn(),
    };
  }
}));

describe('Header', () => {
  it('renders a login link when no user is present', () => {
    render(<Header />);
    const loginLink = screen.getByText(/Login/i);
    expect(loginLink).toBeInTheDocument();
  });
});
