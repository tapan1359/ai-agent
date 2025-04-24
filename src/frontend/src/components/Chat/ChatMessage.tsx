import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface ChatMessageProps {
  role: 'user' | 'assistant'
  content: string
}

export function ChatMessage({ role, content }: ChatMessageProps) {
  return (
    <div 
      className={`p-4 rounded-lg transition-all ${
        role === 'user' 
          ? 'bg-primary-900/30 ml-12 border border-primary-800/30' 
          : 'bg-dark-900/50 mr-12 border border-dark-800'
      }`}
    >
      <div className="flex items-center mb-2">
        <span className={`text-sm font-semibold ${
          role === 'user' 
            ? 'text-primary-400' 
            : 'text-gray-400'
        }`}>
          {role === 'user' ? 'You' : 'Assistant'}
        </span>
      </div>
      <div className="prose prose-invert max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      </div>
    </div>
  )
}
