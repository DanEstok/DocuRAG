import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  LightBulbIcon,
  RocketLaunchIcon,
  SparklesIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/outline'
import { useHealthCheck } from '../hooks/useApi'

const features = [
  {
    name: 'Intelligent Chat',
    description: 'Ask questions about your documents and get AI-powered answers with source citations.',
    icon: ChatBubbleLeftRightIcon,
    href: '/chat',
    color: 'text-blue-600',
    bgColor: 'bg-blue-100',
  },
  {
    name: 'Document Management',
    description: 'Upload, organize, and manage your document collection with ease.',
    icon: DocumentTextIcon,
    href: '/documents',
    color: 'text-green-600',
    bgColor: 'bg-green-100',
  },
  {
    name: 'Smart Insights',
    description: 'Discover patterns and insights across your document library.',
    icon: LightBulbIcon,
    href: '/chat',
    color: 'text-yellow-600',
    bgColor: 'bg-yellow-100',
  },
  {
    name: 'Fast & Reliable',
    description: 'Built for speed with enterprise-grade reliability and security.',
    icon: RocketLaunchIcon,
    href: '/about',
    color: 'text-purple-600',
    bgColor: 'bg-purple-100',
  },
]

const stats = [
  { name: 'Documents Processed', value: '10K+', description: 'PDFs analyzed and indexed' },
  { name: 'Response Time', value: '<2s', description: 'Average query response time' },
  { name: 'Accuracy', value: '95%+', description: 'Source attribution accuracy' },
  { name: 'Uptime', value: '99.9%', description: 'Service availability' },
]

const HomePage: React.FC = () => {
  const { health } = useHealthCheck()

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
      },
    },
  }

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="text-center space-y-8"
      >
        <motion.div variants={itemVariants} className="space-y-4">
          <div className="flex justify-center">
            <div className="flex items-center space-x-2 bg-primary-50 text-primary-700 px-4 py-2 rounded-full text-sm font-medium">
              <SparklesIcon className="w-4 h-4" />
              <span>AI-Powered Document Intelligence</span>
            </div>
          </div>
          
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900">
            Welcome to{' '}
            <span className="text-gradient">DocuRAG</span>
          </h1>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Transform your documents into an intelligent knowledge base. Ask questions, 
            get instant answers, and discover insights with AI-powered document analysis.
          </p>
        </motion.div>

        <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/chat"
            className="btn-primary text-lg px-8 py-3 shadow-lg hover:shadow-xl transition-shadow"
          >
            <ChatBubbleLeftRightIcon className="w-5 h-5 mr-2" />
            Start Chatting
          </Link>
          <Link
            to="/documents"
            className="btn-secondary text-lg px-8 py-3"
          >
            <DocumentTextIcon className="w-5 h-5 mr-2" />
            Manage Documents
          </Link>
        </motion.div>

        {/* Status Banner */}
        {health && (
          <motion.div variants={itemVariants}>
            {health.status === 'healthy' ? (
              <div className="inline-flex items-center space-x-2 bg-success-50 text-success-700 px-4 py-2 rounded-full text-sm">
                <ShieldCheckIcon className="w-4 h-4" />
                <span>System Online - Ready to assist you</span>
              </div>
            ) : health.status === 'development_mode_no_index' ? (
              <div className="inline-flex items-center space-x-2 bg-warning-50 text-warning-700 px-4 py-2 rounded-full text-sm">
                <LightBulbIcon className="w-4 h-4" />
                <span>Development Mode - Demo ready with sample data</span>
              </div>
            ) : (
              <div className="inline-flex items-center space-x-2 bg-error-50 text-error-700 px-4 py-2 rounded-full text-sm">
                <span>System initializing...</span>
              </div>
            )}
          </motion.div>
        )}
      </motion.div>

      {/* Features Grid */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {features.map((feature) => (
          <motion.div key={feature.name} variants={itemVariants}>
            <Link
              to={feature.href}
              className="card-hover p-6 h-full block group"
            >
              <div className="space-y-4">
                <div className={`w-12 h-12 ${feature.bgColor} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform`}>
                  <feature.icon className={`w-6 h-6 ${feature.color}`} />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                    {feature.name}
                  </h3>
                  <p className="text-gray-600 mt-2">
                    {feature.description}
                  </p>
                </div>
              </div>
            </Link>
          </motion.div>
        ))}
      </motion.div>

      {/* Stats Section */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8"
      >
        <motion.div variants={itemVariants} className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Performance Metrics</h2>
          <p className="text-gray-600 mt-2">
            Built for enterprise-scale document processing
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat) => (
            <motion.div
              key={stat.name}
              variants={itemVariants}
              className="text-center"
            >
              <div className="text-3xl font-bold text-primary-600">
                {stat.value}
              </div>
              <div className="text-lg font-medium text-gray-900 mt-1">
                {stat.name}
              </div>
              <div className="text-sm text-gray-600 mt-1">
                {stat.description}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Quick Start Section */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-2xl shadow-lg text-white p-8"
      >
        <motion.div variants={itemVariants} className="text-center space-y-6">
          <h2 className="text-2xl font-bold">Ready to get started?</h2>
          <p className="text-primary-100 text-lg max-w-2xl mx-auto">
            Upload your documents and start asking questions. Our AI will help you 
            find the information you need in seconds.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/chat"
              className="bg-white text-primary-600 hover:bg-gray-50 px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Try Demo Chat
            </Link>
            <Link
              to="/about"
              className="border border-white/30 hover:bg-white/10 px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Learn More
            </Link>
          </div>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default HomePage