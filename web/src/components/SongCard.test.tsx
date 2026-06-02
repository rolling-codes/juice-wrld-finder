import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import SongCard from './SongCard'
import { Song } from '../types'

const mockSong: Song = {
  id: 1,
  title: 'Lucid Dreams',
  slug: 'lucid-dreams',
  release_status: 'released',
  download_status: 'api_link_available',
  notes: 'Original release',
  official_url: 'https://spotify.com/...',
  era_id: 1,
}

function renderWithRouter(component: React.ReactElement) {
  return render(
    <BrowserRouter future={{ v7_relativeSplatPath: true, v7_startTransition: true }}>
      {component}
    </BrowserRouter>,
  )
}

describe('SongCard', () => {
  it('renders song title', () => {
    renderWithRouter(<SongCard song={mockSong} />)
    expect(screen.getByText('Lucid Dreams')).toBeInTheDocument()
  })

  it('displays release status badge', () => {
    renderWithRouter(<SongCard song={mockSong} />)
    expect(screen.getByText('released')).toBeInTheDocument()
  })

  it('displays era badge when era_id is present', () => {
    renderWithRouter(<SongCard song={mockSong} />)
    expect(screen.getByText('Era 1')).toBeInTheDocument()
  })

  it('displays notes when present', () => {
    renderWithRouter(<SongCard song={mockSong} />)
    expect(screen.getByText('Original release')).toBeInTheDocument()
  })

  it('links to song detail page', () => {
    renderWithRouter(<SongCard song={mockSong} />)
    const link = screen.getByRole('link')
    expect(link).toHaveAttribute('href', '/songs/1')
  })

  it('does not display era badge when era_id is null', () => {
    const songWithoutEra = { ...mockSong, era_id: null }
    renderWithRouter(<SongCard song={songWithoutEra} />)
    expect(screen.queryByText(/Era/)).not.toBeInTheDocument()
  })
})
