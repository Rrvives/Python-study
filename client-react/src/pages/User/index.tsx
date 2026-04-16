/**
 * 系统管理页面统一从子路由入口进入：
 * - `/system/users` → UserManagementPage
 * - `/system/menu-management` → MenuManagementPage
 *
 * 保留此文件便于 `import('@/pages/User')` 一类 barrel 扩展（当前路由直接引用子页）。
 */
export { default as SystemLayout } from '@/pages/User/SystemLayout'
export { default as UserManagementPage } from '@/pages/User/UserManagementPage'
export { default as MenuManagementPage } from '@/pages/User/MenuManagementPage'
