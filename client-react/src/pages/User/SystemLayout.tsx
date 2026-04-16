import { Outlet } from 'react-router-dom'

/**
 * 系统管理子路由容器：侧栏点进「用户管理 / 路由权限」后在此渲染子页面。
 */
export default function SystemLayout() {
  return <Outlet />
}
