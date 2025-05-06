import { Button } from 'antd'
import { Table } from '@/components/Table'
import type { ColumnsType } from '@/components/Table'
import type { BusinessLogRow } from '@/pages/Audit/Logs/model/types'

const EXPORT_BTN_STYLE = {
  background: '#e6f4ff',
  borderColor: '#91caff',
  color: '#1677ff',
} as const

type LogDataTableProps = {
  columns: ColumnsType<BusinessLogRow>
  dataSource: BusinessLogRow[]
  loading?: boolean
  onExport: () => void
}

export function LogDataTable({
  columns,
  dataSource,
  loading,
  onExport,
}: LogDataTableProps) {
  return (
    <>
      <div style={{ marginBottom: 12 }}>
        <Button type="primary" onClick={onExport} style={EXPORT_BTN_STYLE}>
          导出
        </Button>
      </div>
      <Table<BusinessLogRow>
        rowKey="key"
        loading={loading}
        columns={columns}
        dataSource={dataSource}
        scroll={{ x: 1200 }}
        locale={{ emptyText: '暂无数据' }}
        rowSelection={{ type: 'checkbox' }}
        pagination={{
          showSizeChanger: true,
          showTotal: (total) => `共 ${total} 条`,
        }}
      />
    </>
  )
}
