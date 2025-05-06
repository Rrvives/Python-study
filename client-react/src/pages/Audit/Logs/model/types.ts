export type LogMainTabKey = 'business' | 'alarm' | 'operation'

export type BusinessLogSubTabKey = 'api' | 'ferry'

export type BusinessLogRow = {
  key: string
  index: number
  groupName: string
  interfaceName: string
  direction: string
  externalAddress: string
  requestTime: string
  status: string
  resultDesc: string
}
