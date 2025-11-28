import { useEffect, useState } from 'react'
import { MonitorCard } from '@/components/MonitorCard'
import { IncidentTimeline } from '@/components/IncidentTimeline'
import { Badge } from '@/components/ui/badge'
import type { Monitor, Incident, OverallStatus } from '@/types'
import { Activity, RefreshCw } from 'lucide-react'

function App() {
  const [monitors, setMonitors] = useState<Monitor[]>([])
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [overallStatus, setOverallStatus] = useState<OverallStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())

  const fetchData = async () => {
    try {
      console.log('Fetching status data...')
      const [monitorsRes, incidentsRes, statusRes] = await Promise.all([
        fetch('/api/monitors'),
        fetch('/api/incidents'),
        fetch('/api/status')
      ])

      console.log('Responses received:', {
        monitors: monitorsRes.status,
        incidents: incidentsRes.status,
        status: statusRes.status
      })

      const monitorsData = await monitorsRes.json()
      const incidentsData = await incidentsRes.json()
      const statusData = await statusRes.json()

      console.log('Data parsed:', {
        monitors: monitorsData.monitors?.length,
        incidents: incidentsData.incidents?.length,
        status: statusData.status
      })

      setMonitors(monitorsData.monitors || [])
      setIncidents(incidentsData.incidents || [])
      setOverallStatus(statusData)
      setLastUpdated(new Date())
      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch status data:', error)
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()

    // Auto-refresh every 60 seconds
    const interval = setInterval(fetchData, 60000)

    return () => clearInterval(interval)
  }, [])

  const getOverallStatusConfig = (status: OverallStatus['status']) => {
    switch (status) {
      case 'operational':
        return {
          variant: 'success' as const,
          text: 'All Systems Operational',
          description: 'All services are running smoothly'
        }
      case 'partial_outage':
        return {
          variant: 'warning' as const,
          text: 'Partial Outage',
          description: 'Some services are experiencing issues'
        }
      case 'major_outage':
        return {
          variant: 'destructive' as const,
          text: 'Major Outage',
          description: 'Multiple services are affected'
        }
      case 'unknown':
        return {
          variant: 'info' as const,
          text: 'Status Unknown',
          description: 'Unable to determine system status'
        }
    }
  }

  const formatLastUpdated = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    }).format(date)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex items-center gap-2">
          <RefreshCw className="h-6 w-6 animate-spin text-muted-foreground" />
          <span className="text-muted-foreground">Loading status...</span>
        </div>
      </div>
    )
  }

  const statusConfig = overallStatus ? getOverallStatusConfig(overallStatus.status) : null

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3 mb-4">
            <Activity className="h-8 w-8" />
            <h1 className="text-3xl font-bold">System Status</h1>
          </div>

          {statusConfig && (
            <div className="space-y-2">
              <Badge variant={statusConfig.variant} className="text-sm px-3 py-1">
                {statusConfig.text}
              </Badge>
              <p className="text-sm text-muted-foreground">
                {statusConfig.description}
              </p>
              <p className="text-xs text-muted-foreground">
                Last updated: {formatLastUpdated(lastUpdated)}
              </p>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="space-y-8">
          {/* Services Section */}
          <section>
            <h2 className="text-2xl font-semibold mb-4">Services</h2>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {monitors.map((monitor) => (
                <MonitorCard key={monitor.id} monitor={monitor} />
              ))}
            </div>
          </section>

          {/* Incidents Section */}
          <section>
            <IncidentTimeline incidents={incidents} />
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t mt-12">
        <div className="container mx-auto px-4 py-6">
          <p className="text-sm text-muted-foreground text-center">
            Powered by Datadog Monitors | Auto-refreshes every 60 seconds
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
