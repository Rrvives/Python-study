import axios, { type AxiosError } from 'axios'
import { getApiBaseUrl } from '@/constants/config'
import { useAppStore } from '@/store'
import { ApiError } from '@/utils/ApiError'
import { notifyUnauthorized } from '@/utils/authEvents'

function pickMessage(data: unknown, fallback: string): string {
  if (data && typeof data === 'object' && 'message' in data) {
    const m = (data as { message: unknown }).message
    if (typeof m === 'string' && m.trim()) return m
  }
  if (data && typeof data === 'object' && 'detail' in data) {
    const d = (data as { detail: unknown }).detail
    if (typeof d === 'string' && d.trim()) return d
  }
  return fallback
}

export const request = axios.create({
  baseURL: getApiBaseUrl() || undefined,
  timeout: 30_000,
  headers: {
    Accept: 'application/json',
  },
})

request.interceptors.request.use((config) => {
  const { token, username } = useAppStore.getState()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  if (username) {
    config.headers['X-Auth-Username'] = username
  }
  return config
})

request.interceptors.response.use(
  (res) => res,
  (error: AxiosError<unknown>) => {
    const status = error.response?.status ?? 0
    const data = error.response?.data
    if (status === 401) {
      notifyUnauthorized()
    }
    const message = pickMessage(
      data,
      error.message || `请求失败（HTTP ${status || '网络'}）`,
    )
    return Promise.reject(new ApiError(message, status, data))
  },
)
