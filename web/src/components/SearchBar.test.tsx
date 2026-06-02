import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SearchBar from './SearchBar'

describe('SearchBar', () => {
  it('renders input with placeholder', () => {
    const mockHandler = vi.fn()
    render(<SearchBar onSearch={mockHandler} />)
    expect(screen.getByPlaceholderText('Search songs...')).toBeInTheDocument()
  })

  it('calls onSearch with input value on change', async () => {
    const user = userEvent.setup()
    const mockHandler = vi.fn()
    render(<SearchBar onSearch={mockHandler} />)

    const input = screen.getByPlaceholderText('Search songs...')
    await user.type(input, 'lucid')

    expect(mockHandler).toHaveBeenCalledWith('lucid')
  })

  it('uses custom placeholder when provided', () => {
    const mockHandler = vi.fn()
    render(<SearchBar onSearch={mockHandler} placeholder="Find a song..." />)
    expect(screen.getByPlaceholderText('Find a song...')).toBeInTheDocument()
  })

  it('updates input value when user types', async () => {
    const user = userEvent.setup()
    const mockHandler = vi.fn()
    render(<SearchBar onSearch={mockHandler} />)

    const input = screen.getByPlaceholderText('Search songs...') as HTMLInputElement
    await user.type(input, 'test')

    expect(input.value).toBe('test')
  })
})
