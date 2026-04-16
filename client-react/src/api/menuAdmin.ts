import { request } from '@/utils/request'

export type ManagedMenuRow = {
  id: number
  menuKey: string
  label: string
  path: string
  componentKey: string
  parentId: number | null
  parentKey: string | null
  level: 1 | 2
  sort: number
  isEnabled: boolean
  allowedUserIds: number[]
}

export type UpsertManagedMenuPayload = {
  menu_key: string
  label: string
  path?: string
  component_key?: string
  parent_id?: number | null
  sort?: number
  is_enabled?: boolean
  allowed_user_ids?: number[]
}

export function fetchManagedMenus() {
  return request
    .get<{ configVersion: string | null; items: ManagedMenuRow[] }>(
      '/navigation/managed-menus',
    )
    .then((res) => res.data)
}

export function createManagedMenu(payload: UpsertManagedMenuPayload) {
  return request.post<ManagedMenuRow>('/navigation/managed-menus', payload).then((res) => res.data)
}

export function patchManagedMenu(
  id: number,
  payload: Partial<UpsertManagedMenuPayload>,
) {
  return request.patch<ManagedMenuRow>(`/navigation/managed-menus/${id}`, payload).then((res) => res.data)
}

export function deleteManagedMenu(id: number) {
  return request.delete<{ id: number; deleted: boolean }>(`/navigation/managed-menus/${id}`).then((res) => res.data)
}
