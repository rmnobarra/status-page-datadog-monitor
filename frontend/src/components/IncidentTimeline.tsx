import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { Incident } from "@/types"
import { AlertCircle, CheckCircle2, Search, Eye } from "lucide-react"

interface IncidentTimelineProps {
  incidents: Incident[]
}

export function IncidentTimeline({ incidents }: IncidentTimelineProps) {
  const getSeverityConfig = (severity: Incident['severity']) => {
    switch (severity) {
      case 'critical':
        return { variant: 'destructive' as const, text: 'Critical' }
      case 'major':
        return { variant: 'warning' as const, text: 'Major' }
      case 'minor':
        return { variant: 'secondary' as const, text: 'Minor' }
    }
  }

  const getStatusConfig = (status: Incident['status']) => {
    switch (status) {
      case 'investigating':
        return { icon: Search, text: 'Investigating', color: 'text-blue-600' }
      case 'identified':
        return { icon: Eye, text: 'Identified', color: 'text-yellow-600' }
      case 'monitoring':
        return { icon: AlertCircle, text: 'Monitoring', color: 'text-orange-600' }
      case 'resolved':
        return { icon: CheckCircle2, text: 'Resolved', color: 'text-green-600' }
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  }

  if (incidents.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Incident History</CardTitle>
          <CardDescription>Past incidents and updates from the last 30 days</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <CheckCircle2 className="h-12 w-12 text-green-500 mb-4" />
            <p className="text-lg font-medium text-muted-foreground">No incidents reported</p>
            <p className="text-sm text-muted-foreground mt-1">All systems have been operating normally</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Incident History</CardTitle>
        <CardDescription>Past incidents and updates from the last 30 days</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {incidents.map((incident) => {
          const statusConfig = getStatusConfig(incident.status)
          const StatusIcon = statusConfig.icon
          const severityConfig = getSeverityConfig(incident.severity)

          return (
            <div key={incident.id} className="border-l-2 border-gray-200 pl-6 pb-6 last:pb-0 relative">
              <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-background border-2 border-gray-300" />

              <div className="space-y-3">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-semibold text-base">{incident.title}</h3>
                      <Badge variant={severityConfig.variant} className="text-xs">
                        {severityConfig.text}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Incident ID: {incident.id}
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      Affected: {incident.affected_services.join(', ')}
                    </p>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <StatusIcon className={`h-4 w-4 ${statusConfig.color}`} />
                    <span className={`font-medium ${statusConfig.color}`}>
                      {statusConfig.text}
                    </span>
                  </div>
                </div>

                <div className="space-y-3 mt-4">
                  {incident.updates.slice().reverse().map((update, index) => {
                    const updateStatusConfig = getStatusConfig(update.status)
                    const UpdateIcon = updateStatusConfig.icon

                    return (
                      <div key={index} className="bg-muted/50 rounded-lg p-3 space-y-1">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <UpdateIcon className={`h-3.5 w-3.5 ${updateStatusConfig.color}`} />
                            <span className={`text-xs font-medium uppercase tracking-wide ${updateStatusConfig.color}`}>
                              {updateStatusConfig.text}
                            </span>
                          </div>
                          <span className="text-xs text-muted-foreground">
                            {formatDate(update.timestamp)}
                          </span>
                        </div>
                        <p className="text-sm text-foreground pl-5">{update.message}</p>
                      </div>
                    )
                  })}
                </div>

                <div className="flex items-center gap-4 text-xs text-muted-foreground pt-2">
                  <span>Started: {formatDate(incident.created_at)}</span>
                  {incident.resolved_at && (
                    <span>Resolved: {formatDate(incident.resolved_at)}</span>
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}
