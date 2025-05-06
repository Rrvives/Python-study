import { Button, Col, DatePicker, Row, Select, Space } from 'antd'
import { Form } from '@/components/Form'
import type { FormInstance } from '@/components/Form'

type LogFilterFormProps = {
  form: FormInstance
  onSearch: () => void
  onReset: () => void
}

export function LogFilterForm({ form, onSearch, onReset }: LogFilterFormProps) {
  return (
    <Form form={form} layout="vertical" requiredMark={false}>
      <Row gutter={16}>
        <Col xs={24} sm={12} lg={6}>
          <Form.Item name="groupName" label="业务组名称">
            <Select allowClear placeholder="请选择" options={[]} />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Form.Item name="interfaceName" label="数据接口名称">
            <Select allowClear placeholder="请选择" options={[]} />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Form.Item name="externalAddress" label="对外服务数据接口地址">
            <Select allowClear placeholder="请选择" options={[]} />
          </Form.Item>
        </Col>
        <Col
          xs={24}
          sm={12}
          lg={6}
          style={{
            display: 'flex',
            alignItems: 'flex-end',
            justifyContent: 'flex-end',
          }}
        >
          <Form.Item label=" ">
            <Space>
              <Button type="primary" onClick={onSearch}>
                查询
              </Button>
              <Button onClick={onReset}>重置</Button>
            </Space>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} lg={8}>
          <Form.Item name="requestTime" label="请求时间">
            <DatePicker.RangePicker style={{ width: '100%' }} showTime />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Form.Item name="requestStatus" label="请求状态">
            <Select allowClear placeholder="请选择" options={[]} />
          </Form.Item>
        </Col>
      </Row>
    </Form>
  )
}
