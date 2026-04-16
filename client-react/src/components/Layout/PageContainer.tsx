import type { ReactNode } from 'react'

type PageContainerProps = {
  title?: string
  children: ReactNode
}

/** 无业务语义的页面容器，可按设计系统扩展 */
export function PageContainer({ title, children }: PageContainerProps) {
  return (
    <div style={{ padding: 16 }}>
      {title ? <h2 style={{ marginTop: 0 }}>{title}</h2> : null}
      {children}
    </div>
  )
}
