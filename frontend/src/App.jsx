import { useState } from 'react'
import SearchBar from './components/SearchBar'
import Roadmap from './components/Roadmap'
import { SkillTree, StrategySection, ResourceList } from './components/ContentWidgets'

function App() {
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (role) => {
    setIsLoading(true)
    setError(null)
    setData(null)

    try {
      // Note: Assuming backend runs on 8000
      const response = await fetch('http://localhost:8000/api/generate-guide', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role })
      })

      if (!response.ok) throw new Error('Failed to fetch guide')

      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen pb-12 transition-colors duration-500">
      <div className="container">
        {/* Navigation / Header */}
        <header className="flex justify-between items-center py-6">
          <div className="font-serif font-bold text-xl tracking-tight text-gray-800">
            Mentor<span className="text-gray-400">.ai</span>
          </div>
        </header>

        {/* Hero Section */}
        <div className={`transition-all duration-700 ${data ? 'mt-4 mb-8' : 'mt-24'}`}>
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>

        {/* Error State */}
        {error && (
          <div className="max-w-md mx-auto p-4 bg-red-50 text-red-600 rounded-lg text-center">
            {error}
          </div>
        )}

        {/* Results Grid */}
        {data && (
          <div className="animate-fade-in space-y-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-serif text-gray-800 mb-2">{data.title}</h2>
              <p className="text-gray-500 max-w-2xl mx-auto">{data.summary}</p>
            </div>

            <div className="bento-grid">
              {/* Row 1: Roadmap (Dominant) & Resources */}
              <div className="col-span-8 row-span-2">
                <Roadmap chart={data.roadmap_mermaid} />
              </div>

              <div className="col-span-4">
                <SkillTree skills={data.skills} />
              </div>

              <div className="col-span-4">
                <ResourceList resources={data.resources} />
              </div>

              {/* Row 2: Strategy (Full width or split) */}
              <div className="col-span-12">
                <StrategySection strategy={data.strategy} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
