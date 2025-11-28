export interface Monitor {
  id: number
  name: string
  description: string
  status: 'OK' | 'Alert' | 'Warn' | 'No Data' | 'Skipped'
}

export interface IncidentUpdate {
  timestamp: string
  status: 'investigating' | 'identified' | 'monitoring' | 'resolved'
  message: string
}

export interface Incident {
  id: string
  title: string
  status: 'investigating' | 'identified' | 'monitoring' | 'resolved'
  severity: 'minor' | 'major' | 'critical'
  created_at: string
  resolved_at: string | null
  affected_services: string[]
  updates: IncidentUpdate[]
}

export interface OverallStatus {
  status: 'operational' | 'partial_outage' | 'major_outage' | 'unknown'
  updated_at: string
}
