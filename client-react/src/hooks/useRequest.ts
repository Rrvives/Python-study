import { useCallback, useState } from 'react'

type AsyncState<T> = {
  data: T | null
  loading: boolean
  error: Error | null
}

/**
 * 简单异步请求状态；复杂场景可换 TanStack Query。
 */
export function useRequest<T>(fetcher: () => Promise<T>) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: false,
    error: null,
  })

  const run = useCallback(async () => {
    setState((s) => ({ ...s, loading: true, error: null }))
    try {
      const data = await fetcher()
      setState({ data, loading: false, error: null })
      return data
    } catch (e) {
      const error = e instanceof Error ? e : new Error(String(e))
      setState((s) => ({ ...s, loading: false, error }))
      throw error
    }
  }, [fetcher])

  return { ...state, run }
}
