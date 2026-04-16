import { request } from '@/utils/request'

/** 后端用户列表行 */
export type AppUserRow = {
  id: number
  username: string
  email: string
  is_active: boolean
  is_superuser: boolean
}

export type UserMenuPermissionRow = {
  id: number
  menuKey: string
  label: string
  parentId: number | null
  parentKey: string | null
  level: 1 | 2
  sort: number
  isEnabled: boolean
}

export function fetchUsers() {
  return request.get<{ users: AppUserRow[] }>('/users').then((res) => res.data.users)
}

export type CreateUserPayload = {
  username: string
  password: string
  email?: string
}

export function createUser(payload: CreateUserPayload) {
  return request.post<AppUserRow>('/users', payload).then((res) => res.data)
}

export type PatchUserPayload = {
  password?: string
  is_active?: boolean
}

export function patchUser(userId: number, payload: PatchUserPayload) {
  return request.patch<AppUserRow>(`/users/${userId}`, payload).then((res) => res.data)
}

export function fetchUserMenuPermissions(userId: number) {
  return request
    .get<{
      configVersion: string | null
      selectedMenuIds: number[]
      items: UserMenuPermissionRow[]
    }>(`/users/${userId}/menu-permissions`)
    .then((res) => res.data)
}

export function patchUserMenuPermissions(userId: number, menuIds: number[]) {
  return request
    .patch<{ userId: number; selectedMenuIds: number[] }>(
      `/users/${userId}/menu-permissions`,
      { menu_ids: menuIds },
    )
    .then((res) => res.data)
}
