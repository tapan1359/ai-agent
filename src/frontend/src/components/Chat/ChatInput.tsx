interface ChatInputProps {
  prompt: string
  isLoading: boolean
  onPromptChange: (value: string) => void
  onSubmit: (e: React.FormEvent) => void
}

export function ChatInput({ prompt, isLoading, onPromptChange, onSubmit }: ChatInputProps) {
  return (
    <form onSubmit={onSubmit} className="relative">
      <input
        type="text"
        value={prompt}
        onChange={(e) => onPromptChange(e.target.value)}
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
  )
}
