import type { LogMainTabKey } from '@/pages/Audit/Logs/model/types'

export const LOG_MAIN_TAB_ITEMS: { key: LogMainTabKey; label: string }[] = [
  { key: 'business', label: '业务日志' },
  { key: 'alarm', label: '告警日志' },
  { key: 'operation', label: '操作日志' },
]
