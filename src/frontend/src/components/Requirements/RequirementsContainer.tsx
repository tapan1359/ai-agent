export function RequirementsContainer() {
  return (
    <div className="h-full flex flex-col">
      <div className="space-y-6 mb-8 flex-1 overflow-y-auto rounded-lg bg-dark-800 p-6">
        <h2 className="text-xl font-semibold text-primary-400">AWS Requirements Input</h2>
        <p className="text-gray-400">
          This tab will contain a form to collect AWS infrastructure requirements across different Well-Architected Framework pillars.
        </p>
      </div>
    </div>
  )
}
