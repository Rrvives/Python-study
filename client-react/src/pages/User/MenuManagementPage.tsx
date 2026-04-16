import { useCallback, useEffect, useMemo, useState } from 'react'
import { Button, Card, Form, Input, Modal, Popconfirm, Result, Select, Space, Switch, Typography, message } from 'antd'
import type { ColumnsType } from '@/components/Table'
import { Table } from '@/components/Table'
import { useUserStore } from '@/store'
import { ApiError } from '@/utils/ApiError'
import { fetchUsers } from '@/api/user'
import type { AppUserRow } from '@/api/user'
import { defaultMenuItems } from '@/layout/menuConfig'
import {
  createManagedMenu,
  deleteManagedMenu,
  fetchManagedMenus,
  patchManagedMenu,
  type ManagedMenuRow,
} from '@/api/menuAdmin'

const { Title, Paragraph } = Typography

type MenuFormValues = {
  menu_key: string
  label: string
  path?: string
  component_key?: string
  sort?: number
  is_enabled?: boolean
  allowed_user_ids?: number[]
}

type EditingState =
  | { mode: 'create-root' }
  | { mode: 'create-child'; parent: ManagedMenuRow }
  | { mode: 'edit'; row: ManagedMenuRow }

type LocalMenuTreeRow = {
  id: string
  menuKey: string
  label: string
  parentKey: string | null
  level: number
  children?: LocalMenuTreeRow[]
}

/** 超级管理员菜单配置：维护一级/二级菜单，并按组分配可见范围。 */
export default function MenuManagementPage() {
  const isSuperuser = useUserStore((s) => s.isSuperuser)
  const [loading, setLoading] = useState(false)
  const [rows, setRows] = useState<ManagedMenuRow[]>([])
  const [users, setUsers] = useState<AppUserRow[]>([])
  const [editing, setEditing] = useState<EditingState | null>(null)
  const [form] = Form.useForm<MenuFormValues>()

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const [menusResp, userRows] = await Promise.all([fetchManagedMenus(), fetchUsers()])
      setRows(menusResp.items ?? [])
      setUsers(userRows)
    } catch (e) {
      message.error(e instanceof ApiError ? e.message : '加载菜单配置失败')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (isSuperuser) {
      void loadData()
    }
  }, [isSuperuser, loadData])

  const userOptions = useMemo(
    () =>
      users
        .filter((u) => u.is_active)
        .map((u) => ({ label: `${u.username}${u.is_superuser ? '（超管）' : ''}`, value: u.id })),
    [users],
  )

  type TreeRow = ManagedMenuRow & { children?: TreeRow[] }
  const treeRows = useMemo<TreeRow[]>(() => {
    const list = [...rows].sort((a, b) => a.sort - b.sort || a.id - b.id)
    const byId = new Map<number, TreeRow>()
    for (const row of list) {
      byId.set(row.id, { ...row, children: [] })
    }
    const roots: TreeRow[] = []
    for (const row of list) {
      const node = byId.get(row.id)!
      if (row.parentId && byId.has(row.parentId)) {
        byId.get(row.parentId)!.children!.push(node)
      } else {
        roots.push(node)
      }
    }
    for (const node of byId.values()) {
      if (!node.children?.length) {
        delete node.children
      }
    }
    return roots
  }, [rows])

  const localMenuTree = useMemo<LocalMenuTreeRow[]>(() => {
    const walk = (
      nodes: typeof defaultMenuItems,
      parentKey: string | null,
      level: number,
      scope: string,
    ): LocalMenuTreeRow[] =>
      (nodes ?? [])
        .map((node, idx) => {
          if (!node || typeof node !== 'object') return null
          const key = (node as { key?: unknown }).key
          if (typeof key !== 'string') return null
          const labelRaw = (node as { label?: unknown }).label
          const label = typeof labelRaw === 'string' ? labelRaw : key
          const childrenRaw = (node as { children?: typeof defaultMenuItems }).children
          const rowId = `${scope}:${parentKey ?? 'root'}:${key}:${idx}`
          const children = Array.isArray(childrenRaw)
            ? walk(childrenRaw, key, level + 1, scope)
            : []
          const row: LocalMenuTreeRow = {
            id: rowId,
            menuKey: key,
            label,
            parentKey,
            level,
          }
          if (children.length) {
            row.children = children
          }
          return row
        })
        .filter((x): x is LocalMenuTreeRow => Boolean(x))

    return walk(defaultMenuItems, null, 1, 'default')
  }, [])

  const openCreateRoot = () => {
    setEditing({ mode: 'create-root' })
  }

  const openCreateChild = (parent: ManagedMenuRow) => {
    setEditing({ mode: 'create-child', parent })
  }

  const openEdit = (row: ManagedMenuRow) => {
    setEditing({ mode: 'edit', row })
  }

  const fillMenuForm = (target: EditingState | null) => {
    if (!target) {
      form.resetFields()
      return
    }
    if (target.mode === 'edit') {
      form.setFieldsValue({
        menu_key: target.row.menuKey,
        label: target.row.label,
        path: target.row.path,
        component_key: target.row.componentKey,
        sort: target.row.sort,
        is_enabled: target.row.isEnabled,
        allowed_user_ids: target.row.allowedUserIds,
      })
      return
    }
    form.setFieldsValue({
      menu_key: '',
      label: '',
      path: '',
      component_key: '',
      sort: 0,
      is_enabled: true,
      allowed_user_ids: [],
    })
  }

  useEffect(() => {
    fillMenuForm(editing)
  }, [editing, form])

  const submit = async () => {
    if (!editing) return
    try {
      const values = await form.validateFields()
      if (editing.mode === 'edit') {
        await patchManagedMenu(editing.row.id, {
          menu_key: values.menu_key.trim(),
          label: values.label.trim(),
          path: values.path?.trim() ?? '',
          component_key: values.component_key?.trim() ?? '',
          sort: values.sort ?? 0,
          is_enabled: values.is_enabled ?? true,
          allowed_user_ids: values.allowed_user_ids ?? [],
        })
        message.success('菜单已更新')
      } else {
        await createManagedMenu({
          menu_key: values.menu_key.trim(),
          label: values.label.trim(),
          path: values.path?.trim() ?? '',
          component_key: values.component_key?.trim() ?? '',
          sort: values.sort ?? 0,
          is_enabled: values.is_enabled ?? true,
          allowed_user_ids: values.allowed_user_ids ?? [],
          parent_id: editing.mode === 'create-child' ? editing.parent.id : null,
        })
        message.success('菜单已创建')
      }
      setEditing(null)
      await loadData()
    } catch (e) {
      if (e && typeof e === 'object' && 'errorFields' in e) return
      message.error(e instanceof ApiError ? e.message : '保存失败')
    }
  }

  const remove = async (row: ManagedMenuRow) => {
    try {
      await deleteManagedMenu(row.id)
      message.success('菜单已删除')
      await loadData()
    } catch (e) {
      message.error(e instanceof ApiError ? e.message : '删除失败')
    }
  }

  const columns: ColumnsType<ManagedMenuRow> = [
    { title: 'ID', dataIndex: 'id', width: 70 },
    {
      title: '层级',
      width: 100,
      render: (_: unknown, row: ManagedMenuRow) => (row.level === 1 ? '一级菜单' : '二级菜单'),
    },
    { title: '菜单Key', dataIndex: 'menuKey', width: 200 },
    {
      title: '标题（父级可折叠展开）',
      dataIndex: 'label',
    },
    {
      title: '父级',
      render: (_: unknown, row: ManagedMenuRow) => row.parentKey ?? '-',
      width: 180,
    },
    { title: '路由路径', dataIndex: 'path', width: 200 },
    { title: '组件Key', dataIndex: 'componentKey', width: 180 },
    {
      title: '可见用户',
      render: (_: unknown, row: ManagedMenuRow) => {
        if (!row.allowedUserIds.length) return '全员'
        return row.allowedUserIds
          .map((id) => users.find((u) => u.id === id)?.username ?? String(id))
          .join(', ')
      },
    },
    {
      title: '操作',
      width: 220,
      fixed: 'right',
      render: (_: unknown, row: ManagedMenuRow) => (
        <Space size={4}>
          {row.level === 1 ? (
            <Button type="link" onClick={() => openCreateChild(row)}>
              新增二级
            </Button>
          ) : null}
          <Button type="link" onClick={() => openEdit(row)}>
            编辑
          </Button>
          <Popconfirm
            title="确认删除该菜单？"
            description="删除一级菜单会级联删除其二级菜单。"
            onConfirm={() => void remove(row)}
          >
            <Button type="link" danger>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const localColumns: ColumnsType<LocalMenuTreeRow> = [
    { title: '层级', dataIndex: 'level', width: 100, render: (v: number) => `第${v}级` },
    { title: '菜单Key', dataIndex: 'menuKey', width: 240 },
    { title: '菜单标题', dataIndex: 'label' },
    { title: '父级Key', dataIndex: 'parentKey', width: 200, render: (v: string | null) => v ?? '-' },
  ]

  if (!isSuperuser) {
    return (
      <div style={{ padding: 16 }}>
        <Result
          status="403"
          title="仅超级管理员可配置菜单"
          subTitle="当前账号不是 superuser，无法执行菜单维护与菜单分配。"
        />
      </div>
    )
  }

  return (
    <div style={{ padding: 16 }}>
      <Title level={4} style={{ marginTop: 0 }}>
        菜单管理
      </Title>
      <Paragraph type="secondary">
        支持维护一级/二级菜单，并按用户分配菜单显示/隐藏。未分配的用户将不显示该菜单（超级管理员除外）。
      </Paragraph>
      <Card variant="borderless" style={{ marginBottom: 16 }}>
        <Typography.Title level={5} style={{ marginTop: 0 }}>
          系统内置菜单（只读，显示所有默认菜单）
        </Typography.Title>
        <Table<LocalMenuTreeRow>
          rowKey="id"
          columns={localColumns}
          dataSource={localMenuTree}
          pagination={false}
          expandable={{
            rowExpandable: (record) => Boolean(record.children?.length),
          }}
        />
      </Card>
      <Card variant="borderless">
        <Typography.Title level={5} style={{ marginTop: 0 }}>
          受控菜单（可配置显示/隐藏）
        </Typography.Title>
        <Space style={{ marginBottom: 12 }}>
          <Button type="primary" onClick={openCreateRoot}>
            新增一级菜单
          </Button>
          <Button onClick={() => void loadData()} loading={loading}>
            刷新
          </Button>
        </Space>
        <Table<ManagedMenuRow>
          rowKey="id"
          columns={columns}
          dataSource={treeRows}
          loading={loading}
          scroll={{ x: 1400 }}
          pagination={false}
          expandable={{
            rowExpandable: (record) => Boolean((record as TreeRow).children?.length),
          }}
        />
      </Card>

      <Modal
        title={
          editing?.mode === 'create-root'
            ? '新增一级菜单'
            : editing?.mode === 'create-child'
              ? `新增二级菜单（父级：${editing.parent.label}）`
              : editing?.mode === 'edit'
                ? `编辑菜单：${editing.row.label}`
                : ''
        }
        open={Boolean(editing)}
        forceRender
        afterOpenChange={(open) => {
          if (open) fillMenuForm(editing)
        }}
        onOk={() => void submit()}
        onCancel={() => setEditing(null)}
        destroyOnClose
      >
        <Form form={form} layout="vertical" preserve={false}>
          <Form.Item name="menu_key" label="菜单Key" rules={[{ required: true }]}>
            <Input placeholder="如：/system/users 或 system-management" />
          </Form.Item>
          <Form.Item name="label" label="标题" rules={[{ required: true }]}>
            <Input placeholder="菜单显示名称" />
          </Form.Item>
          <Form.Item name="path" label="路由Path">
            <Input placeholder="可选，建议与 key 一致（如 /system/users）" />
          </Form.Item>
          <Form.Item name="component_key" label="组件Key">
            <Input placeholder="可选，需在 routeRegistry 中注册" />
          </Form.Item>
          <Form.Item name="sort" label="排序" initialValue={0}>
            <Input type="number" />
          </Form.Item>
          <Form.Item name="is_enabled" label="启用" valuePropName="checked" initialValue={true}>
            <Switch />
          </Form.Item>
          <Form.Item name="allowed_user_ids" label="可见用户">
            <Select
              mode="multiple"
              allowClear
              options={userOptions}
              placeholder="不选则全员可见"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}
