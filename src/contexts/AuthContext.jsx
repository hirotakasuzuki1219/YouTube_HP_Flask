import { createContext, useState, useEffect, useContext } from 'react'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const response = await fetch('/api/check-auth', {
        credentials: 'include'
      })
      const data = await response.json()
      setIsAuthenticated(data.authenticated)
    } catch (error) {
      console.error('認証チェックエラー:', error)
      setIsAuthenticated(false)
    } finally {
      setLoading(false)
    }
  }

  const login = async (password) => {
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ password })
      })
      const data = await response.json()
      
      if (data.success) {
        setIsAuthenticated(true)
        return { success: true }
      } else {
        return { success: false, error: data.error || 'ログインに失敗しました' }
      }
    } catch (error) {
      return { success: false, error: 'ネットワークエラーが発生しました' }
    }
  }

  const logout = async () => {
    try {
      await fetch('/api/logout', {
        method: 'POST',
        credentials: 'include'
      })
      setIsAuthenticated(false)
    } catch (error) {
      console.error('ログアウトエラー:', error)
      setIsAuthenticated(false)
    }
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading, login, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

