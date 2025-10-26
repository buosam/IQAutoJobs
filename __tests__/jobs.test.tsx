
import { render, screen, fireEvent, act } from '@testing-library/react';
import JobsContent from '../src/app/jobs/jobs-content';
import { useRouter, useSearchParams } from 'next/navigation';

// Mock the next/navigation module
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
  useSearchParams: jest.fn(),
}));

// Mock global fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ jobs: [], total: 0, page: 1, size: 20, pages: 0 }),
  })
);

describe('JobsContent', () => {
  let pushMock;

  beforeEach(() => {
    pushMock = jest.fn();
    (useRouter as jest.Mock).mockReturnValue({ push: pushMock });
    (useSearchParams as jest.Mock).mockReturnValue(new URLSearchParams());
    (fetch as jest.Mock).mockClear();
  });

  it('should call router.push on search', async () => {
    await act(async () => {
      render(<JobsContent />);
    });

    const searchInput = screen.getByPlaceholderText('Search jobs, companies, or keywords...');
    const searchButton = screen.getByRole('button', { name: /Search/i });

    fireEvent.change(searchInput, { target: { value: 'developer' } });
    fireEvent.submit(searchButton.closest('form'));

    expect(pushMock).toHaveBeenCalledTimes(1);
    expect(pushMock).toHaveBeenCalledWith('/jobs?search=developer&page=1');
  });

  it('should call router.push on pagination change', async () => {
    // Setup search params to show pagination
    const params = new URLSearchParams();
    params.set('page', '1');
    (useSearchParams as jest.Mock).mockReturnValue(params);

    // Mock fetch to return multiple pages
    (fetch as jest.Mock).mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ jobs: [ { id: '1', title: 'Job 1', company: { id: '1', name: 'Company 1' } } ], total: 40, page: 1, size: 20, pages: 2 }),
      })
    );

    await act(async () => {
      render(<JobsContent />);
    });


    const nextPageButton = await screen.findByRole('button', { name: '2' });
    fireEvent.click(nextPageButton);

    expect(pushMock).toHaveBeenCalledTimes(1);
    expect(pushMock).toHaveBeenCalledWith('/jobs?page=2');
  });
});
