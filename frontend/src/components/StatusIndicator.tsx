import React from 'react'
import { motion } from 'framer-motion'
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline'
import { HealthResponse } from '../utils/api'

interface StatusIndicatorProps {
  health: HealthResponse | null
  loading: boolean
  compact?: boolean
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({ health, loading, compact = false }) => {
  const getStatusInfo = () => {
    if (loading) {
      return {
        icon: ArrowPathIcon,
        text: 'Checking...',
        color: 'text-gray-500',
        bgColor: 'bg-gray-100',
        badge: 'badge-info',
      }
    }

    if (!health) {
      return {
        icon: XCircleIcon,
        text: 'Offline',
        color: 'text-error-600',
        bgColor: 'bg-error-100',
        badge: 'badge-error',
      }
    }

    switch (health.status) {
      case 'healthy':
        return {
          icon: CheckCircleIcon,
          text: 'Online',
          color: 'text-success-600',
          bgColor: 'bg-success-100',
          badge: 'badge-success',
        }
      case 'development_mode_no_index':
        return {
          icon: ExclamationTriangleIcon,
          text: 'Dev Mode',
          color: 'text-warning-600',
          bgColor: 'bg-warning-100',
          badge: 'badge-warning',
        }
      default:
        return {
          icon: ExclamationTriangleIcon,
          text: 'Issues',
          color: 'text-warning-600',
          bgColor: 'bg-warning-100',
          badge: 'badge-warning',
        }
    }
  }

  const { icon: Icon, text, color, bgColor, badge } = getStatusInfo()

  if (compact) {
    return (
      <div className="flex items-center space-x-2">
        <motion.div
          animate={{ rotate: loading ? 360 : 0 }}
          transition={{ duration: 1, repeat: loading ? Infinity : 0, ease: 'linear' }}
          className={`w-2 h-2 rounded-full ${bgColor}`}
        />
        <span className={`text-sm font-medium ${color}`}>{text}</span>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center space-x-2">
        <motion.div
          animate={{ rotate: loading ? 360 : 0 }}
          transition={{ duration: 1, repeat: loading ? Infinity : 0, ease: 'linear' }}
        >
          <Icon className={`w-5 h-5 ${color}`} />
        </motion.div>
        <span className={`text-sm font-medium ${color}`}>API Status</span>
      </div>
      
      <div className={`badge ${badge}`}>
        {text}
      </div>
      
      {health && (
        <div className="text-xs text-gray-500">
          Version {health.version}
        </div>
      )}
      
      {health?.status === 'development_mode_no_index' && (
        <div className="text-xs text-warning-600 bg-warning-50 p-2 rounded border border-warning-200">
          Running in development mode. Create test data to enable full functionality.
        </div>
      )}
    </div>
  )
}

export default StatusIndicator