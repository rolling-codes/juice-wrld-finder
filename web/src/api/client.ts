import axios, { AxiosInstance } from 'axios'

const API_BASE = '/api'
const TOKEN_KEY = 'jw_admin_token'

export const client: AxiosInstance = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor to attach JWT token
client.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

// API endpoints
export const api = {
  auth: {
    login: (username: string, password: string) =>
      client.post('/auth/login', { username, password }),
    me: () => client.get('/auth/me'),
  },
  songs: {
    list: (skip = 0, limit = 100, eraId?: number, releaseStatus?: string) => {
      const params: any = { skip, limit }
      if (eraId) params.era_id = eraId
      if (releaseStatus) params.release_status = releaseStatus
      return client.get('/songs', { params })
    },
    get: (id: number) => client.get(`/songs/${id}`),
  },
  search: {
    query: (q: string, skip = 0, limit = 50) =>
      client.get('/search', { params: { q, skip, limit } }),
    lyrics: (q: string, skip = 0, limit = 50) =>
      client.get('/search/lyrics', { params: { q, skip, limit } }),
  },
  eras: {
    list: () => client.get('/eras'),
    get: (id: number) => client.get(`/eras/${id}`),
    songs: (id: number) => client.get(`/eras/${id}/songs`),
  },
  producers: {
    list: () => client.get('/producers'),
  },
  links: {
    public: (songId: number) => client.get(`/links/songs/${songId}`),
    admin: (songId: number) => client.get(`/links/admin/songs/${songId}`),
    create: (songId: number, label: string, url: string, linkType: string, visibility: string) =>
      client.post('/links/admin', { song_id: songId, label, url, link_type: linkType, visibility }),
    update: (id: number, updates: any) =>
      client.patch(`/links/admin/${id}`, updates),
    delete: (id: number) => client.delete(`/links/admin/${id}`),
  },
}
