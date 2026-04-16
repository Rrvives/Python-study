/** 全局常量枚举占位：避免 TS `enum` 与 erasableSyntaxOnly 冲突 */
export const HTTP_STATUS = {
  Unauthorized: 401,
  Forbidden: 403,
  NotFound: 404,
} as const
