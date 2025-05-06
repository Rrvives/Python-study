import { useMemo, useState } from 'react'
import { Form, Radio, message } from 'antd'
import { LogDataTable } from '@/pages/Audit/Logs/components/LogDataTable'
import { LogFilterForm } from '@/pages/Audit/Logs/components/LogFilterForm'
import { getBusinessLogTableColumns } from '@/pages/Audit/Logs/model/columns'
import type {
  BusinessLogRow,
  BusinessLogSubTabKey,
} from '@/pages/Audit/Logs/model/types'

export function BusinessLogPanel() {
  const [form] = Form.useForm()
  const [subTab, setSubTab] = useState<BusinessLogSubTabKey>('api')
  const [loading] = useState(false)
  const [dataSource] = useState<BusinessLogRow[]>([])

  const columns = useMemo(() => getBusinessLogTableColumns(), [])

  const handleSearch = async () => {
    const values = await form.validateFields().catch(() => null)
    if (!values) return
    message.success(
      `已提交查询（示例：${subTab === 'api' ? 'API' : '摆渡'}，无真实接口）`,
    )
  }

  const handleReset = () => {
    form.resetFields()
  }

  const handleExport = () => {
    message.info('导出功能为占位（可对接后端导出接口）')
  }

  return (
    <>
      <div style={{ marginBottom: 16 }}>
        <Radio.Group
          value={subTab}
          onChange={(e) => setSubTab(e.target.value as BusinessLogSubTabKey)}
          optionType="button"
          buttonStyle="solid"
        >
          <Radio.Button value="api">API业务日志</Radio.Button>
          <Radio.Button value="ferry">
            通用应用层数据摆渡业务日志
          </Radio.Button>
        </Radio.Group>
      </div>

      <LogFilterForm form={form} onSearch={handleSearch} onReset={handleReset} />

      <LogDataTable
        columns={columns}
        dataSource={dataSource}
        loading={loading}
        onExport={handleExport}
      />
    </>
  )
}
