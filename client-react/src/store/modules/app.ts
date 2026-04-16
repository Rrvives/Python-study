import { create } from 'zustand'
import {
  getStoredToken,
  getStoredUsername,
  setStoredToken,
  setStoredUsername,
} from '@/utils/auth'

type AppState = {
  token: string | null
  username: string | null
  setToken: (token: string | null) => void
  setUsername: (username: string | null) => void
  clearAuth: () => void
}

const initialToken = getStoredToken()
const initialUsername = getStoredUsername()

export const useAppStore = create<AppState>((set) => ({
  token: initialToken,
  username: initialUsername,
  setToken: (token) => {
    setStoredToken(token)
    set({ token })
  },
  setUsername: (username) => {
    setStoredUsername(username)
    set({ username })
  },
  clearAuth: () => {
    setStoredToken(null)
    setStoredUsername(null)
    set({ token: null, username: null })
  },
}))
