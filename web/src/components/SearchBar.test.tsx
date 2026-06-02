import { describe, it, expect, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import SearchBar from './SearchBar'

describe('SearchBar', () => {
  it('renders input with placeholder', () => {
    const mockHandler = vi.fn()
    render(<SearchBar onSearch={mockHandler} />)
    expect(screen.getByPlaceholderText('Search songs...')).toBeInTheDocument()
  })

  it('calls onSearch when input changes', () => {
    const mockHandler = vi.fn()
    render(<SearchBar onSearch={mockHandler} />)

    const input = screen.getByPlaceholderText('Search songs...')
    fireEvent.change(input, { target: { value: 'l' } })

    expect(mockHandler).toHaveBeenCalled()
  })

  it('uses custom placeholder when provided', () => {
    const mockHandler = vi.fn()
    render(<SearchBar onSearch={mockHandler} placeholder="Find a song..." />)
    expect(screen.getByPlaceholderText('Find a song...')).toBeInTheDocument()
  })

  it('accepts typed input', () => {
    const mockHandler = vi.fn()
    render(<SearchBar onSearch={mockHandler} />)

    const input = screen.getByPlaceholderText('Search songs...') as HTMLInputElement
    fireEvent.change(input, { target: { value: 'test' } })

    expect(input.value).toContain('test')
  })
})
