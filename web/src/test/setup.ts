import '@testing-library/jest-dom'
import { afterEach, vi } from 'vitest'
import { cleanup } from '@testing-library/react'

afterEach(() => {
  cleanup()
})

vi.mock('../api/client', () => ({
  api: {
    songs: {
      list: vi.fn(),
      get: vi.fn(),
    },
    eras: {
      list: vi.fn(),
      get: vi.fn(),
      songs: vi.fn(),
    },
    search: {
      query: vi.fn(),
      lyrics: vi.fn(),
    },
    links: {
      public: vi.fn(),
    },
  },
}))
