import type { ReactNode } from 'react'
import { Suspense } from 'react'
import { Spin } from 'antd'

type RouteSuspenseProps = {
  children: ReactNode
}

export function RouteSuspense({ children }: RouteSuspenseProps) {
  return (
    <Suspense
      fallback={
        <Spin size="large" style={{ display: 'block', margin: '120px auto' }} />
      }
    >
      {children}
    </Suspense>
  )
}
