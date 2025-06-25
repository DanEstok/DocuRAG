import React from 'react'
import { motion } from 'framer-motion'
import {
  SparklesIcon,
  RocketLaunchIcon,
  ShieldCheckIcon,
  GlobeAltIcon,
  CodeBracketIcon,
  HeartIcon,
  ArrowTopRightOnSquareIcon,
} from '@heroicons/react/24/outline'

const AboutPage: React.FC = () => {
  const features = [
    {
      icon: SparklesIcon,
      title: 'AI-Powered Search',
      description: 'Advanced natural language processing to understand your questions and find relevant information.',
    },
    {
      icon: RocketLaunchIcon,
      title: 'Fast & Scalable',
      description: 'Built for performance with efficient vector search and optimized AI inference.',
    },
    {
      icon: ShieldCheckIcon,
      title: 'Secure & Private',
      description: 'Your documents stay private with local processing and enterprise-grade security.',
    },
    {
      icon: GlobeAltIcon,
      title: 'Modern Interface',
      description: 'Clean, intuitive design that makes document AI accessible to everyone.',
    },
  ]

  const techStack = [
    { name: 'FastAPI', description: 'High-performance Python web framework' },
    { name: 'LangChain', description: 'Framework for building AI applications' },
    { name: 'OpenAI GPT', description: 'State-of-the-art language models' },
    { name: 'FAISS', description: 'Efficient vector similarity search' },
    { name: 'React', description: 'Modern frontend framework' },
    { name: 'TypeScript', description: 'Type-safe JavaScript development' },
    { name: 'Tailwind CSS', description: 'Utility-first CSS framework' },
    { name: 'Docker', description: 'Containerized deployment' },
  ]

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
        className="text-center space-y-6"
      >
        <motion.div variants={itemVariants}>
          <div className="w-20 h-20 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-glow">
            <SparklesIcon className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            About <span className="text-gradient">DocuRAG</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            DocuRAG is an intelligent document analysis platform that combines the power of 
            AI with modern web technology to make your documents searchable and interactive.
          </p>
        </motion.div>
      </motion.div>

      {/* Mission Statement */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-2xl p-8"
      >
        <motion.div variants={itemVariants} className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Our Mission</h2>
          <p className="text-lg text-gray-700 max-w-4xl mx-auto">
            We believe that information should be accessible and actionable. DocuRAG transforms 
            static documents into dynamic knowledge bases, enabling you to have conversations 
            with your content and discover insights that would otherwise remain hidden.
          </p>
        </motion.div>
      </motion.div>

      {/* Features Grid */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
      >
        <motion.div variants={itemVariants} className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Key Features</h2>
          <p className="text-gray-600">
            Powerful capabilities designed for modern document workflows
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature) => (
            <motion.div
              key={feature.title}
              variants={itemVariants}
              className="card p-6"
            >
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <feature.icon className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Technology Stack */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="card p-8"
      >
        <motion.div variants={itemVariants} className="text-center mb-8">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <CodeBracketIcon className="w-6 h-6 text-primary-600" />
            <h2 className="text-2xl font-bold text-gray-900">Technology Stack</h2>
          </div>
          <p className="text-gray-600">
            Built with modern, proven technologies for reliability and performance
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {techStack.map((tech) => (
            <motion.div
              key={tech.name}
              variants={itemVariants}
              className="bg-gray-50 rounded-lg p-4 text-center hover:bg-gray-100 transition-colors"
            >
              <h3 className="font-semibold text-gray-900 mb-1">{tech.name}</h3>
              <p className="text-sm text-gray-600">{tech.description}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Architecture Overview */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="space-y-8"
      >
        <motion.div variants={itemVariants} className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">How It Works</h2>
          <p className="text-gray-600 max-w-3xl mx-auto">
            DocuRAG uses a sophisticated pipeline to process your documents and enable intelligent search
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <motion.div variants={itemVariants} className="text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-blue-600">1</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Document Processing</h3>
            <p className="text-gray-600">
              PDFs are parsed, chunked, and converted into vector embeddings using advanced NLP models.
            </p>
          </motion.div>
          
          <motion.div variants={itemVariants} className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-green-600">2</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Intelligent Search</h3>
            <p className="text-gray-600">
              Your questions are matched against document content using semantic similarity search.
            </p>
          </motion.div>
          
          <motion.div variants={itemVariants} className="text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-purple-600">3</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Response</h3>
            <p className="text-gray-600">
              Relevant content is sent to AI models to generate accurate, contextual answers with citations.
            </p>
          </motion.div>
        </div>
      </motion.div>

      {/* Open Source */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="bg-gray-900 text-white rounded-2xl p-8"
      >
        <motion.div variants={itemVariants} className="text-center space-y-6">
          <div className="flex items-center justify-center space-x-2">
            <HeartIcon className="w-6 h-6 text-red-400" />
            <h2 className="text-2xl font-bold">Open Source</h2>
          </div>
          <p className="text-gray-300 max-w-3xl mx-auto">
            DocuRAG is open source and available on GitHub. We believe in transparency, 
            community collaboration, and making AI accessible to everyone.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="https://github.com/your-username/DocuRAG"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-6 py-3 bg-white text-gray-900 rounded-lg font-medium hover:bg-gray-100 transition-colors"
            >
              <CodeBracketIcon className="w-5 h-5 mr-2" />
              View on GitHub
              <ArrowTopRightOnSquareIcon className="w-4 h-4 ml-2" />
            </a>
            <a
              href="https://github.com/your-username/DocuRAG/blob/main/docs/contributing.md"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-6 py-3 border border-gray-600 text-white rounded-lg font-medium hover:bg-gray-800 transition-colors"
            >
              Contributing Guide
              <ArrowTopRightOnSquareIcon className="w-4 h-4 ml-2" />
            </a>
          </div>
        </motion.div>
      </motion.div>

      {/* Version Info */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="text-center text-sm text-gray-500"
      >
        <motion.div variants={itemVariants}>
          <p>DocuRAG v1.0.0 • Built with ❤️ for the AI community</p>
          <p className="mt-1">
            © 2024 DocuRAG Project • Licensed under MIT License
          </p>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default AboutPage