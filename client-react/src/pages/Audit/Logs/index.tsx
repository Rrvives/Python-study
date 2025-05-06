import { useState } from 'react'
import { Breadcrumb, Card, Tabs } from 'antd'
import { BusinessLogPanel } from '@/pages/Audit/Logs/components/BusinessLogPanel'
import { LogTabPlaceholder } from '@/pages/Audit/Logs/components/LogTabPlaceholder'
import { LOG_MAIN_TAB_ITEMS } from '@/pages/Audit/Logs/constants/logTabs'
import type { LogMainTabKey } from '@/pages/Audit/Logs/model/types'

export default function LogManagementPage() {
  const [mainTab, setMainTab] = useState<LogMainTabKey>('business')

  return (
    <div style={{ padding: 16 }}>
      <Breadcrumb
        style={{ marginBottom: 16 }}
        items={[{ title: '审计管理' }, { title: '日志管理' }]}
      />

      <Card bordered={false} styles={{ body: { padding: 16 } }}>
        <Tabs
          activeKey={mainTab}
          onChange={(key) => setMainTab(key as LogMainTabKey)}
          items={LOG_MAIN_TAB_ITEMS.map(({ key, label }) => ({
            key,
            label,
          }))}
        />

        {mainTab === 'business' && <BusinessLogPanel />}

        {mainTab === 'alarm' && (
          <LogTabPlaceholder description="告警日志（占位，可按同样结构接接口）" />
        )}

        {mainTab === 'operation' && (
          <LogTabPlaceholder description="操作日志（占位，可按同样结构接接口）" />
        )}
      </Card>
    </div>
  )
}
