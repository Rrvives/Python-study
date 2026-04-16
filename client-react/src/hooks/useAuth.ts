import { useAppStore } from '@/store'

export function useAuth() {
  const token = useAppStore((s) => s.token)
  const username = useAppStore((s) => s.username)
  const setToken = useAppStore((s) => s.setToken)
  const setUsername = useAppStore((s) => s.setUsername)
  const clearAuth = useAppStore((s) => s.clearAuth)

  return {
    token,
    username,
    isAuthenticated: Boolean(token || username),
    setToken,
    setUsername,
    clearAuth,
  }
}
