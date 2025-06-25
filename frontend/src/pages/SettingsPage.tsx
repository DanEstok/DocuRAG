import React from 'react'
import { motion } from 'framer-motion'
import {
  Cog6ToothIcon,
  ComputerDesktopIcon,
  GlobeAltIcon,
  ShieldCheckIcon,
  BellIcon,
} from '@heroicons/react/24/outline'
import { useLocalStorage, useHealthCheck } from '../hooks/useApi'
import { toast } from 'react-hot-toast'

interface SettingOption {
  value: string
  label: string
}

interface BaseSetting {
  label: string
  description: string
}

interface SelectSetting extends BaseSetting {
  type: 'select'
  value: string
  onChange: (value: string) => void
  options: SettingOption[]
}

interface ToggleSetting extends BaseSetting {
  type: 'toggle'
  value: boolean
  onChange: (value: boolean) => void
}

interface NumberSetting extends BaseSetting {
  type: 'number'
  value: number
  onChange: (value: number) => void
  min: number
  max: number
}

type Setting = SelectSetting | ToggleSetting | NumberSetting

interface SettingSection {
  title: string
  icon: React.ComponentType<{ className?: string }>
  settings: Setting[]
}

const SettingsPage: React.FC = () => {
  const { health } = useHealthCheck()
  const [theme, setTheme] = useLocalStorage('theme', 'light')
  const [notifications, setNotifications] = useLocalStorage('notifications', true)
  const [autoRefresh, setAutoRefresh] = useLocalStorage('autoRefresh', true)
  const [maxResults, setMaxResults] = useLocalStorage('maxResults', 10)
  const [responseFormat, setResponseFormat] = useLocalStorage('responseFormat', 'detailed')

  const handleSave = () => {
    toast.success('Settings saved successfully!')
  }

  const settingSections: SettingSection[] = [
    {
      title: 'Appearance',
      icon: ComputerDesktopIcon,
      settings: [
        {
          label: 'Theme',
          description: 'Choose your preferred color scheme',
          type: 'select' as const,
          value: theme,
          onChange: setTheme,
          options: [
            { value: 'light', label: 'Light' },
            { value: 'dark', label: 'Dark' },
            { value: 'auto', label: 'Auto' },
          ],
        },
      ],
    },
    {
      title: 'Chat Settings',
      icon: GlobeAltIcon,
      settings: [
        {
          label: 'Response Format',
          description: 'How detailed should AI responses be',
          type: 'select' as const,
          value: responseFormat,
          onChange: setResponseFormat,
          options: [
            { value: 'brief', label: 'Brief' },
            { value: 'detailed', label: 'Detailed' },
            { value: 'comprehensive', label: 'Comprehensive' },
          ],
        },
        {
          label: 'Maximum Results',
          description: 'Number of source documents to retrieve',
          type: 'number' as const,
          value: maxResults,
          onChange: setMaxResults,
          min: 1,
          max: 20,
        },
      ],
    },
    {
      title: 'System',
      icon: ShieldCheckIcon,
      settings: [
        {
          label: 'Auto-refresh Status',
          description: 'Automatically check system health',
          type: 'toggle' as const,
          value: autoRefresh,
          onChange: setAutoRefresh,
        },
        {
          label: 'Notifications',
          description: 'Show system notifications and alerts',
          type: 'toggle' as const,
          value: notifications,
          onChange: setNotifications,
        },
      ],
    },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Customize your DocuRAG experience</p>
      </div>

      {/* System Information */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Cog6ToothIcon className="w-5 h-5 mr-2" />
          System Information
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">API Status</p>
            <p className="font-semibold text-gray-900">
              {health?.status === 'healthy' ? 'Online' : 
               health?.status === 'development_mode_no_index' ? 'Dev Mode' : 
               'Offline'}
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Version</p>
            <p className="font-semibold text-gray-900">{health?.version || 'Unknown'}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Environment</p>
            <p className="font-semibold text-gray-900">
              {health?.status === 'development_mode_no_index' ? 'Development' : 'Production'}
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Last Check</p>
            <p className="font-semibold text-gray-900">Just now</p>
          </div>
        </div>
      </div>

      {/* Settings Sections */}
      <div className="space-y-6">
        {settingSections.map((section, sectionIndex) => (
          <motion.div
            key={section.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: sectionIndex * 0.1 }}
            className="card p-6"
          >
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <section.icon className="w-5 h-5 mr-2" />
              {section.title}
            </h2>
            
            <div className="space-y-6">
              {section.settings.map((setting) => (
                <div key={setting.label} className="flex items-center justify-between">
                  <div className="flex-1">
                    <label className="text-sm font-medium text-gray-900">
                      {setting.label}
                    </label>
                    <p className="text-sm text-gray-600">{setting.description}</p>
                  </div>
                  
                  <div className="ml-4">
                    {setting.type === 'toggle' && (
                      <button
                        onClick={() => (setting as ToggleSetting).onChange(!(setting as ToggleSetting).value)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          (setting as ToggleSetting).value ? 'bg-primary-600' : 'bg-gray-200'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            (setting as ToggleSetting).value ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    )}
                    
                    {setting.type === 'select' && (
                      <select
                        value={(setting as SelectSetting).value}
                        onChange={(e) => (setting as SelectSetting).onChange(e.target.value)}
                        className="input w-32"
                      >
                        {(setting as SelectSetting).options.map((option) => (
                          <option key={option.value} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                      </select>
                    )}
                    
                    {setting.type === 'number' && (
                      <input
                        type="number"
                        value={(setting as NumberSetting).value}
                        onChange={(e) => (setting as NumberSetting).onChange(parseInt(e.target.value))}
                        min={(setting as NumberSetting).min}
                        max={(setting as NumberSetting).max}
                        className="input w-20"
                      />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Advanced Settings */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Advanced Settings</h2>
        <div className="space-y-4">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <BellIcon className="w-5 h-5 text-yellow-600" />
              <span className="font-medium text-yellow-800">Development Mode</span>
            </div>
            <p className="text-sm text-yellow-700">
              You're currently running in development mode with mock AI responses. 
              To enable full AI capabilities, configure your OpenAI API key in production mode.
            </p>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-900">Clear Chat History</label>
              <p className="text-sm text-gray-600">Remove all stored conversations</p>
            </div>
            <button className="btn-danger">
              Clear History
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-900">Reset Settings</label>
              <p className="text-sm text-gray-600">Restore all settings to defaults</p>
            </div>
            <button className="btn-secondary">
              Reset All
            </button>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button onClick={handleSave} className="btn-primary">
          Save Settings
        </button>
      </div>

      {/* Keyboard Shortcuts */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Keyboard Shortcuts</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Send message</span>
              <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Enter</kbd>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">New line</span>
              <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Shift + Enter</kbd>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Clear chat</span>
              <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl + K</kbd>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Go to chat</span>
              <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl + 1</kbd>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Go to documents</span>
              <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl + 2</kbd>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Go to settings</span>
              <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl + 3</kbd>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SettingsPage