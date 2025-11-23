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
      if (!response.ok) {
        console.error('認証チェック失敗:', response.status, response.statusText)
        setIsAuthenticated(false)
        setLoading(false)
        return
      }
      const data = await response.json()
      console.log('認証状態:', data)
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
      
      if (!response.ok) {
        console.error('ログイン失敗:', response.status, response.statusText)
        const errorData = await response.json().catch(() => ({}))
        return { success: false, error: errorData.error || 'ログインに失敗しました' }
      }
      
      const data = await response.json()
      console.log('ログイン結果:', data)
      
      if (data.success) {
        setIsAuthenticated(true)
        return { success: true }
      } else {
        return { success: false, error: data.error || 'ログインに失敗しました' }
      }
    } catch (error) {
      console.error('ログインエラー:', error)
      return { success: false, error: 'ネットワークエラーが発生しました: ' + error.message }
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



