import { useCallback, useEffect, useState } from 'react'
import type { ColumnsType } from '@/components/Table'
import { Table } from '@/components/Table'
import type { AppUserRow, UserMenuPermissionRow } from '@/api/user'
import {
  createUser,
  fetchUserMenuPermissions,
  fetchUsers,
  patchUser,
  patchUserMenuPermissions,
} from '@/api/user'
import { ApiError } from '@/utils/ApiError'
import { Button, Form, Input, Modal, Select, Space, Switch, Tag, Typography, message } from 'antd'

type CreateFormValues = {
  username: string
  password: string
  email?: string
}

type EditFormValues = {
  password?: string
  menu_ids?: number[]
  is_active: boolean
}

export function UserList() {
  const [rows, setRows] = useState<AppUserRow[]>([])
  const [menuPermissionRows, setMenuPermissionRows] = useState<UserMenuPermissionRow[]>([])
  const [menuSelectedIds, setMenuSelectedIds] = useState<number[]>([])
  const [loading, setLoading] = useState(false)
  const [menuLoading, setMenuLoading] = useState(false)
  const [createOpen, setCreateOpen] = useState(false)
  const [editOpen, setEditOpen] = useState(false)
  const [editing, setEditing] = useState<AppUserRow | null>(null)
  const [createForm] = Form.useForm<CreateFormValues>()
  const [editForm] = Form.useForm<EditFormValues>()
  const { Text } = Typography

  const loadAll = useCallback(async () => {
    setLoading(true)
    try {
      const u = await fetchUsers()
      setRows(u)
    } catch (e) {
      message.error(e instanceof ApiError ? e.message : '加载失败')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void loadAll()
  }, [loadAll])

  const openEdit = async (record: AppUserRow) => {
    setEditing(record)
    setEditOpen(true)
    setMenuLoading(true)
    setMenuPermissionRows([])
    setMenuSelectedIds([])
    try {
      const menuResp = await fetchUserMenuPermissions(record.id)
      setMenuPermissionRows(menuResp.items ?? [])
      setMenuSelectedIds(menuResp.selectedMenuIds ?? [])
    } catch (e) {
      setMenuPermissionRows([])
      setMenuSelectedIds([])
      message.error(e instanceof ApiError ? e.message : '加载菜单权限失败')
    } finally {
      setMenuLoading(false)
    }
  }

  const fillUserEditForm = (record: AppUserRow | null, menuIds: number[]) => {
    if (!record) {
      editForm.resetFields()
      return
    }
    editForm.setFieldsValue({
      password: '',
      is_active: record.is_active,
      menu_ids: menuIds,
    })
  }

  useEffect(() => {
    if (!editOpen || !editing) return
    fillUserEditForm(editing, menuSelectedIds)
  }, [editOpen, editing, editForm])

  useEffect(() => {
    if (!editOpen) return
    fillUserEditForm(editing, menuSelectedIds)
  }, [editOpen, menuSelectedIds, editForm])

  const columns: ColumnsType<AppUserRow> = [
    { title: 'ID', dataIndex: 'id', width: 72 },
    { title: '用户名', dataIndex: 'username', width: 140 },
    { title: '邮箱', dataIndex: 'email', ellipsis: true },
    {
      title: '状态',
      width: 160,
      render: (_: unknown, r: AppUserRow) => (
        <Space direction="vertical" size={0}>
          <span>{r.is_active ? '启用' : '停用'}</span>
          {r.is_superuser && <Tag color="red">超级管理员</Tag>}
        </Space>
      ),
    },
    {
      title: '操作',
      width: 100,
      fixed: 'right',
      render: (_: unknown, r: AppUserRow) => (
        <Button type="link" onClick={() => void openEdit(r)}>
          编辑
        </Button>
      ),
    },
  ]

  const submitCreate = async () => {
    try {
      const v = await createForm.validateFields()
      await createUser({
        username: v.username.trim(),
        password: v.password,
        email: v.email?.trim(),
      })
      message.success('用户已创建')
      setCreateOpen(false)
      createForm.resetFields()
      await loadAll()
    } catch (e) {
      if (e && typeof e === 'object' && 'errorFields' in e) return
      message.error(e instanceof ApiError ? e.message : '创建失败')
    }
  }

  const submitEdit = async () => {
    if (!editing) return
    try {
      const v = await editForm.validateFields()
      const payload: Parameters<typeof patchUser>[1] = {}
      if (editing.is_superuser) {
        if (!v.password?.trim()) {
          message.error('超级管理员只能修改密码，且密码不能为空')
          return
        }
        payload.password = v.password.trim()
      } else {
        payload.is_active = v.is_active
        if (v.password?.trim()) {
          payload.password = v.password.trim()
        }
      }
      await patchUser(editing.id, payload)
      if (!editing.is_superuser) {
        await patchUserMenuPermissions(editing.id, v.menu_ids ?? [])
      }
      message.success('已保存')
      setEditOpen(false)
      setEditing(null)
      await loadAll()
    } catch (e) {
      if (e && typeof e === 'object' && 'errorFields' in e) return
      message.error(e instanceof ApiError ? e.message : '保存失败')
    }
  }

  return (
    <div>
      <Space style={{ marginBottom: 12 }}>
        <Button type="primary" onClick={() => setCreateOpen(true)}>
          添加用户
        </Button>
        <Button onClick={() => void loadAll()} loading={loading}>
          刷新
        </Button>
      </Space>
      <Table<AppUserRow>
        rowKey="id"
        columns={columns}
        dataSource={rows}
        loading={loading}
        scroll={{ x: 900 }}
      />

      <Modal
        title="添加用户"
        open={createOpen}
        onOk={() => void submitCreate()}
        onCancel={() => {
          setCreateOpen(false)
          createForm.resetFields()
        }}
        destroyOnClose
      >
        <Form form={createForm} layout="vertical" preserve={false}>
          <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
            <Input placeholder="登录名" />
          </Form.Item>
          <Form.Item name="password" label="密码" rules={[{ required: true, min: 6 }]}>
            <Input.Password placeholder="至少 6 位" />
          </Form.Item>
          <Form.Item name="email" label="邮箱">
            <Input />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={editing ? `编辑：${editing.username}` : '编辑'}
        open={editOpen}
        forceRender
        afterOpenChange={(open) => {
          if (open) fillUserEditForm(editing, menuSelectedIds)
        }}
        onOk={() => void submitEdit()}
        onCancel={() => {
          setEditOpen(false)
          setEditing(null)
          setMenuPermissionRows([])
          setMenuSelectedIds([])
          editForm.resetFields()
        }}
        destroyOnClose
      >
        <Form form={editForm} layout="vertical" preserve={false}>
          <Form.Item
            name="password"
            label={editing?.is_superuser ? '新密码（超级管理员仅可修改密码）' : '新密码（留空则不修改）'}
            rules={editing?.is_superuser ? [{ required: true, min: 6 }] : undefined}
          >
            <Input.Password placeholder="留空表示不修改" />
          </Form.Item>
          {!editing?.is_superuser ? (
            <Form.Item name="menu_ids" label="菜单权限（显示/隐藏）">
              <Select
                mode="multiple"
                allowClear
                loading={menuLoading}
                placeholder="不选则该用户看不到受控菜单"
                options={menuPermissionRows
                  .sort((a, b) => a.sort - b.sort || a.id - b.id)
                  .map((m) => ({
                    value: m.id,
                    label: `${m.level === 2 ? '└─ ' : ''}${m.label} (${m.menuKey})`,
                  }))}
              />
            </Form.Item>
          ) : (
            <Text type="secondary">超级管理员账号仅允许修改密码，其他字段已锁定。</Text>
          )}
          {!editing?.is_superuser ? (
            <Form.Item name="is_active" label="启用账号" valuePropName="checked" rules={[{ required: true }]}>
              <Switch />
            </Form.Item>
          ) : null}
        </Form>
      </Modal>
    </div>
  )
}
