import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

function App() {
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant', content: string }[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim() || isLoading) return

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: prompt }])
    setIsLoading(true)
    setPrompt('')

    try {
      const response = await fetch(import.meta.env.VITE_API_URL + '/assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({
          prompt,
          stream: true
        })
      })

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) throw new Error('No reader available')

      // Add initial assistant message with loading state
      setMessages(prev => [...prev, { role: 'assistant', content: 'Thinking...' }])

      let assistantResponse = ''
      let hasStartedReceiving = false

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data:')) {
            try {
              const data = JSON.parse(line.slice(5))
              if (data.content) {
                hasStartedReceiving = true
                assistantResponse = data.content
                setMessages(prev => {
                  const newMessages = [...prev]
                  newMessages[newMessages.length - 1].content = assistantResponse
                  return newMessages
                })
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e)
            }
          }
        }
      }

      // If we never received a response, show an error
      if (!hasStartedReceiving) {
        setMessages(prev => {
          const newMessages = [...prev]
          newMessages[newMessages.length - 1].content = 'Sorry, I encountered an error while processing your request.'
          return newMessages
        })
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, there was an error processing your request.' 
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-900 text-gray-100 font-mono">
      <div className="max-w-4xl mx-auto p-4">
        <header className="py-6 mb-8 border-b border-dark-800">
          <h1 className="text-2xl font-bold text-primary-400">AI Assistant</h1>
        </header>

        {/* Messages Container */}
        <div className="space-y-6 mb-8 h-[60vh] overflow-y-auto rounded-lg bg-dark-800 p-6">
          {messages.map((message, index) => (
            <div 
              key={index} 
              className={`p-4 rounded-lg transition-all ${
                message.role === 'user' 
                  ? 'bg-primary-900/30 ml-12 border border-primary-800/30' 
                  : 'bg-dark-900/50 mr-12 border border-dark-800'
              }`}
            >
              <div className="flex items-center mb-2">
                <span className={`text-sm font-semibold ${
                  message.role === 'user' 
                    ? 'text-primary-400' 
                    : 'text-gray-400'
                }`}>
                  {message.role === 'user' ? 'You' : 'Assistant'}
                </span>
              </div>
              <div className="prose prose-invert max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content}
                </ReactMarkdown>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="relative">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask me anything..."
            className="w-full p-4 pr-24 bg-dark-800 border border-dark-800 rounded-lg focus:outline-none focus:border-primary-600 transition-colors"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className={`absolute right-2 top-2 px-4 py-2 bg-primary-600 text-white rounded-lg transition-all ${
              isLoading 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:bg-primary-500'
            }`}
          >
            {isLoading ? 'Thinking...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App
