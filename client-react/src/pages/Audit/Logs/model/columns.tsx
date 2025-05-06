import type { ColumnsType } from 'antd/es/table'
import type { BusinessLogRow } from '@/pages/Audit/Logs/model/types'

export function getBusinessLogTableColumns(): ColumnsType<BusinessLogRow> {
  return [
    { title: '序号', dataIndex: 'index', width: 72, align: 'center' },
    {
      title: '业务组名称',
      dataIndex: 'groupName',
      ellipsis: true,
      width: 140,
    },
    {
      title: '数据接口名称',
      dataIndex: 'interfaceName',
      ellipsis: true,
      width: 160,
    },
    {
      title: '数据接口方向',
      dataIndex: 'direction',
      width: 120,
    },
    {
      title: '对外服务数据接口地址',
      dataIndex: 'externalAddress',
      ellipsis: true,
      width: 220,
    },
    {
      title: '请求时间',
      dataIndex: 'requestTime',
      width: 180,
    },
    {
      title: '请求状态',
      dataIndex: 'status',
      width: 100,
    },
    {
      title: '请求结果描述',
      dataIndex: 'resultDesc',
      ellipsis: true,
    },
    {
      title: '操作',
      key: 'action',
      width: 88,
      fixed: 'right',
      render: () => <a>详情</a>,
    },
  ]
}
