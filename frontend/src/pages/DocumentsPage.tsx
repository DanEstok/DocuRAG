import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  DocumentTextIcon,
  ArrowUpTrayIcon,
  ArrowPathIcon,
  FolderIcon,
  InformationCircleIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'
import { refreshIndex } from '../utils/api'
import { useHealthCheck } from '../hooks/useApi'
import LoadingSpinner from '../components/LoadingSpinner'

const DocumentsPage: React.FC = () => {
  const [isRefreshing, setIsRefreshing] = useState(false)
  const { health } = useHealthCheck()

  const handleRefreshIndex = async () => {
    setIsRefreshing(true)
    try {
      const response = await refreshIndex()
      toast.success(`Index refreshed! Processed ${response.documents_processed} documents.`)
    } catch (error) {
      console.error('Refresh failed:', error)
      toast.error('Failed to refresh index')
    } finally {
      setIsRefreshing(false)
    }
  }

  const documentStats = [
    { name: 'Total Documents', value: '12', icon: DocumentTextIcon, color: 'text-blue-600' },
    { name: 'Indexed Pages', value: '248', icon: FolderIcon, color: 'text-green-600' },
    { name: 'Last Updated', value: '2 hours ago', icon: ArrowPathIcon, color: 'text-purple-600' },
  ]

  const sampleDocuments = [
    {
      name: 'Machine Learning Guide',
      type: 'PDF',
      size: '2.4 MB',
      pages: 45,
      lastModified: '2024-01-15',
      status: 'indexed',
    },
    {
      name: 'AI Ethics Research',
      type: 'PDF',
      size: '1.8 MB',
      pages: 32,
      lastModified: '2024-01-14',
      status: 'indexed',
    },
    {
      name: 'Data Science Handbook',
      type: 'PDF',
      size: '3.2 MB',
      pages: 67,
      lastModified: '2024-01-13',
      status: 'indexed',
    },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Document Management</h1>
          <p className="text-gray-600">Manage your document collection and search index</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={handleRefreshIndex}
            disabled={isRefreshing}
            className="btn-secondary"
          >
            {isRefreshing ? (
              <LoadingSpinner size="sm" />
            ) : (
              <ArrowPathIcon className="w-4 h-4" />
            )}
            <span className="ml-2">Refresh Index</span>
          </button>
          <button className="btn-primary">
            <ArrowUpTrayIcon className="w-4 h-4 mr-2" />
            Upload Documents
          </button>
        </div>
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">System Status</h2>
            <div className="space-y-4">
              {health ? (
                <div className="flex items-center space-x-3">
                  {health.status === 'healthy' ? (
                    <>
                      <CheckCircleIcon className="w-6 h-6 text-success-600" />
                      <div>
                        <p className="font-medium text-gray-900">System Online</p>
                        <p className="text-sm text-gray-600">All services are running normally</p>
                      </div>
                    </>
                  ) : health.status === 'development_mode_no_index' ? (
                    <>
                      <ExclamationTriangleIcon className="w-6 h-6 text-warning-600" />
                      <div>
                        <p className="font-medium text-gray-900">Development Mode</p>
                        <p className="text-sm text-gray-600">Running with mock data and test documents</p>
                      </div>
                    </>
                  ) : (
                    <>
                      <ExclamationTriangleIcon className="w-6 h-6 text-error-600" />
                      <div>
                        <p className="font-medium text-gray-900">System Issues</p>
                        <p className="text-sm text-gray-600">Some services may not be available</p>
                      </div>
                    </>
                  )}
                </div>
              ) : (
                <div className="flex items-center space-x-3">
                  <LoadingSpinner size="sm" />
                  <p className="text-gray-600">Checking system status...</p>
                </div>
              )}
              
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-2">Quick Actions</h3>
                <div className="space-y-2 text-sm">
                  <p className="text-gray-600">
                    • Upload new PDF documents to expand your knowledge base
                  </p>
                  <p className="text-gray-600">
                    • Refresh the index after adding new documents
                  </p>
                  <p className="text-gray-600">
                    • Monitor processing status and system health
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {/* Stats */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Statistics</h2>
            <div className="space-y-4">
              {documentStats.map((stat) => (
                <div key={stat.name} className="flex items-center space-x-3">
                  <div className={`w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center`}>
                    <stat.icon className={`w-4 h-4 ${stat.color}`} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">{stat.name}</p>
                    <p className="font-semibold text-gray-900">{stat.value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Info */}
          <div className="card p-6">
            <div className="flex items-center space-x-2 mb-3">
              <InformationCircleIcon className="w-5 h-5 text-blue-600" />
              <h3 className="font-medium text-gray-900">Information</h3>
            </div>
            <div className="text-sm text-gray-600 space-y-2">
              <p>
                Documents are automatically processed and indexed for AI search.
              </p>
              <p>
                Supported formats: PDF files up to 50MB each.
              </p>
              <p>
                Processing time varies based on document size and complexity.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Document List */}
      <div className="card">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Document Library</h2>
          <p className="text-sm text-gray-600">
            {health?.status === 'development_mode_no_index' 
              ? 'Sample documents for development and testing'
              : 'Your uploaded documents and their processing status'
            }
          </p>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Document
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Size
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Pages
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Modified
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {sampleDocuments.map((doc, index) => (
                <motion.tr
                  key={doc.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="hover:bg-gray-50"
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <DocumentTextIcon className="w-5 h-5 text-gray-400 mr-3" />
                      <div>
                        <div className="text-sm font-medium text-gray-900">{doc.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {doc.type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {doc.size}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {doc.pages}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="badge badge-success">
                      {doc.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {doc.lastModified}
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {sampleDocuments.length === 0 && (
          <div className="text-center py-12">
            <DocumentTextIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No documents found</h3>
            <p className="text-gray-600 mb-6">
              Upload your first document to get started with AI-powered search.
            </p>
            <button className="btn-primary">
              <ArrowUpTrayIcon className="w-4 h-4 mr-2" />
              Upload Document
            </button>
          </div>
        )}
      </div>

      {/* Upload Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-medium text-blue-900 mb-2">How to add documents</h3>
        <div className="text-sm text-blue-800 space-y-1">
          <p>1. Click "Upload Documents" to select PDF files from your computer</p>
          <p>2. Wait for the documents to be processed and indexed</p>
          <p>3. Start asking questions about your documents in the Chat section</p>
          <p>4. Use "Refresh Index" if you add documents manually to the server</p>
        </div>
      </div>
    </div>
  )
}

export default DocumentsPage