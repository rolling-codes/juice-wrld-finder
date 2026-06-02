import { useState, useCallback, useEffect } from 'react'
import { api, setToken, clearToken, getToken } from '../api/client'

export function useAuth() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Check if token exists on mount
  useEffect(() => {
    const token = getToken()
    if (token) {
      setIsLoggedIn(true)
      // Try to fetch current user
      api.auth.me()
        .then((res) => {
          setUsername(res.data.username)
        })
        .catch(() => {
          // Token is invalid, clear it
          logout()
        })
        .finally(() => {
          setLoading(false)
        })
    } else {
      setLoading(false)
    }
  }, [])

  const login = useCallback(async (username: string, password: string) => {
    try {
      setError('')
      setLoading(true)
      const res = await api.auth.login(username, password)
      setToken(res.data.access_token)
      setIsLoggedIn(true)
      setUsername(username)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    clearToken()
    setIsLoggedIn(false)
    setUsername('')
  }, [])

  return {
    isLoggedIn,
    username,
    loading,
    error,
    login,
    logout,
  }
}
