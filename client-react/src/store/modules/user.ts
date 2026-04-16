import { create } from 'zustand'

type UserState = {
  displayName: string | null
  /** 登录接口下发的权限标记，用于控制界面（如是否展示「设为 staff」） */
  isSuperuser: boolean | null
  isStaff: boolean | null
  setDisplayName: (name: string | null) => void
  setAuthFlags: (flags: { isSuperuser?: boolean; isStaff?: boolean }) => void
}

export const useUserStore = create<UserState>((set) => ({
  displayName: null,
  isSuperuser: null,
  isStaff: null,
  setDisplayName: (displayName) => set({ displayName }),
  setAuthFlags: (flags) =>
    set({
      isSuperuser: flags.isSuperuser ?? null,
      isStaff: flags.isStaff ?? null,
    }),
}))
