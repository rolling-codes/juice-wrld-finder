import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import FilterBar from './FilterBar'
import * as client from '../api/client'

const mockEras = [
  { id: 1, name: '2018', years: '2018', description: 'First year' },
  { id: 2, name: '2019', years: '2019', description: 'Second year' },
]

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
})

function renderWithQuery(component: React.ReactElement) {
  return render(<QueryClientProvider client={queryClient}>{component}</QueryClientProvider>)
}

describe('FilterBar', () => {
  beforeEach(() => {
    vi.mocked(client.api.eras.list).mockResolvedValue({ data: mockEras } as any)
  })

  it('renders era and release status selects', async () => {
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

    await waitFor(() => {
      expect(screen.getByDisplayValue('All Eras')).toBeInTheDocument()
      expect(screen.getByDisplayValue('All Releases')).toBeInTheDocument()
    })
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

    await waitFor(() => {
      expect(screen.getByText('2018')).toBeInTheDocument()
      expect(screen.getByText('2019')).toBeInTheDocument()
    })
  })

  it('calls onEraChange when era is selected', async () => {
    const user = userEvent.setup()
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

    await waitFor(() => {
      expect(screen.getByText('2018')).toBeInTheDocument()
    })

    const eraSelect = screen.getByDisplayValue('All Eras')
    await user.selectOption(eraSelect, '1')

    expect(mockEraChange).toHaveBeenCalledWith(1)
  })

  it('calls onStatusChange when release status is selected', async () => {
    const user = userEvent.setup()
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

    const statusSelect = screen.getByDisplayValue('All Releases')
    await user.selectOption(statusSelect, 'released')

    expect(mockStatusChange).toHaveBeenCalledWith('released')
  })

  it('shows selected era value', async () => {
    const mockEraChange = vi.fn()
    const mockStatusChange = vi.fn()

    renderWithQuery(
      <FilterBar
        selectedEra={1}
        onEraChange={mockEraChange}
        releaseStatus={null}
        onStatusChange={mockStatusChange}
      />
    )

    await waitFor(() => {
      const eraSelect = screen.getByDisplayValue('1') as HTMLSelectElement
      expect(eraSelect.value).toBe('1')
    })
  })
})
