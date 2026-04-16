import { request } from '@/utils/request'

export type LoginPayload = {
  username: string
  password: string
}

export type LoginResult = {
  accessToken?: string
  username?: string
  displayName?: string
  /** 后端登录接口返回，用于前端控制敏感管理项 */
  isSuperuser?: boolean
  isStaff?: boolean
}

/** 登录：对接后端时调整 path 与字段 */
export function loginApi(payload: LoginPayload) {
  return request.post<LoginResult>('/auth/login', payload).then((res) => res.data)
}
