import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { Monitor } from "@/types"
import { CheckCircle2, AlertCircle, AlertTriangle, HelpCircle, MinusCircle } from "lucide-react"

interface MonitorCardProps {
  monitor: Monitor
}

export function MonitorCard({ monitor }: MonitorCardProps) {
  const getStatusConfig = (status: Monitor['status']) => {
    switch (status) {
      case 'OK':
        return {
          variant: 'success' as const,
          icon: CheckCircle2,
          text: 'Operational',
          className: 'text-green-600'
        }
      case 'Alert':
        return {
          variant: 'destructive' as const,
          icon: AlertCircle,
          text: 'Major Outage',
          className: 'text-red-600'
        }
      case 'Warn':
        return {
          variant: 'warning' as const,
          icon: AlertTriangle,
          text: 'Degraded Performance',
          className: 'text-yellow-600'
        }
      case 'No Data':
        return {
          variant: 'info' as const,
          icon: HelpCircle,
          text: 'No Data',
          className: 'text-gray-600'
        }
      case 'Skipped':
        return {
          variant: 'info' as const,
          icon: MinusCircle,
          text: 'Skipped',
          className: 'text-gray-600'
        }
    }
  }

  const config = getStatusConfig(monitor.status)
  const Icon = config.icon

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-medium">{monitor.name}</CardTitle>
          <Icon className={`h-5 w-5 ${config.className}`} />
        </div>
        <CardDescription>{monitor.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <Badge variant={config.variant}>{config.text}</Badge>
      </CardContent>
    </Card>
  )
}
