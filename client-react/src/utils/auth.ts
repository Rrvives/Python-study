import { storage } from '@/utils/storage'

const TOKEN_KEY = 'access_token'
const USERNAME_KEY = 'username'

/** 持久化 token（可选：与 zustand 内存态配合使用） */
export function getStoredToken(): string | null {
  return storage.get(TOKEN_KEY)
}

export function setStoredToken(token: string | null) {
  if (token) storage.set(TOKEN_KEY, token)
  else storage.remove(TOKEN_KEY)
}

export function getStoredUsername(): string | null {
  return storage.get(USERNAME_KEY)
}

export function setStoredUsername(username: string | null) {
  if (username) storage.set(USERNAME_KEY, username)
  else storage.remove(USERNAME_KEY)
}
