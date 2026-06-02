import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import FilterBar from './FilterBar'
import * as client from '../api/client'

const mockEras = [
  { id: 1, name: '2018', years: '2018', description: 'First year' },
  { id: 2, name: '2019', years: '2019', description: 'Second year' },
]

function renderWithQuery(component: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })
  return render(<QueryClientProvider client={queryClient}>{component}</QueryClientProvider>)
}

describe('FilterBar', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(client.api.eras.list).mockResolvedValue({ data: mockEras } as any)
  })

  it('renders era and release status selects', () => {
    const mockEraChange = vi.fn()
    const mockStatusChange = vi.fn()

    renderWithQuery(
      <FilterBar
        selectedEra={null}
        onEraChange={mockEraChange}
        releaseStatus={null}
        onStatusChange={mockStatusChange}
      />
    )

    expect(screen.getByDisplayValue('All Eras')).toBeInTheDocument()
    expect(screen.getByDisplayValue('All Releases')).toBeInTheDocument()
  })

  it('loads and displays eras from API', async () => {
    const mockEraChange = vi.fn()
    const mockStatusChange = vi.fn()

    renderWithQuery(
      <FilterBar
        selectedEra={null}
        onEraChange={mockEraChange}
        releaseStatus={null}
        onStatusChange={mockStatusChange}
      />
    )

    await waitFor(
      () => {
        expect(screen.getByText('2018')).toBeInTheDocument()
      },
      { timeout: 3000 }
    )
    expect(screen.getByText('2019')).toBeInTheDocument()
  })

  it('displays release status options', () => {
    const mockEraChange = vi.fn()
    const mockStatusChange = vi.fn()

    renderWithQuery(
      <FilterBar
        selectedEra={null}
        onEraChange={mockEraChange}
        releaseStatus={null}
        onStatusChange={mockStatusChange}
      />
    )

    expect(screen.getByRole('option', { name: 'Released' })).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'Unreleased' })).toBeInTheDocument()
  })
})
