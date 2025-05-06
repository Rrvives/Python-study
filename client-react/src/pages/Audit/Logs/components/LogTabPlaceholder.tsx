type LogTabPlaceholderProps = {
  description: string
}

export function LogTabPlaceholder({ description }: LogTabPlaceholderProps) {
  return (
    <div style={{ padding: '48px 0', textAlign: 'center', color: '#999' }}>
      {description}
    </div>
  )
}
