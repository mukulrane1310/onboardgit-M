import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

interface Hotspot {
  file_path: string
  change_count: number
}

interface BusFactorRisk {
  file_path: string
  owner_name: string
  ownership_percent: number
}

interface CoupledFile {
  file_a: string
  file_b: string
  co_change_count: number
}

interface AnalysisResult {
  total_commits: number
  hotspots: Hotspot[]
  bus_factor_risks: BusFactorRisk[]
  coupled_files: CoupledFile[]
}

interface ProjectHistoryItem {
  id: string
  repo_url: string
  status: string
  created_at: string
}

function Dashboard() {
  const { token } = useAuth()
  const [repoUrl, setRepoUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [errorMessage, setErrorMessage] = useState('')
  const [history, setHistory] = useState<ProjectHistoryItem[]>([])

  const fetchHistory = useCallback(async () => {
    try {
      const response = await axios.get(
        'http://127.0.0.1:8000/projects',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      setHistory(response.data)
    } catch (error) {
      console.error('Failed to fetch history:', error)
    }
  }, [token])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchHistory()
  }, [fetchHistory])

  const handleAnalyze = async () => {
    setLoading(true)
    setErrorMessage('')
    setResult(null)

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/analyze',
        {
          repo_url: repoUrl,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      setResult(response.data)
      fetchHistory()
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setErrorMessage(error.response.data.detail)
      } else {
        setErrorMessage('Something went wrong. Please try again.')
      }
    }

    setLoading(false)
  }

  const fetchProjectDetails = async (projectId: string) => {
    setLoading(true)
    setErrorMessage('')

    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/projects/${projectId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      setResult(response.data)
      setRepoUrl(response.data.repo_url)
    } catch {
      setErrorMessage('Could not load this analysis')
    }

    setLoading(false)
  }
  const handleDelete = async (projectId: string, event: React.MouseEvent) => {
     event.stopPropagation()  // Prevents the card's onClick (view details) from also firing

  try {
    await axios.delete(
      `http://127.0.0.1:8000/projects/${projectId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
    fetchHistory()
  } catch (error) {
    console.error('Failed to delete project:', error)
  }
}

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 px-4 py-12">
      <div className="max-w-2xl mx-auto">
        {/* Description */}
<div className="mb-10">
  <p className="text-gray-400">
    Understand any codebase's history before you touch it.
  </p>
</div>

        {/* Input + Button */}
        <div className="flex gap-3 mb-6">
          <input
            type="text"
            placeholder="Enter GitHub repo URL"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
          <button
  onClick={handleAnalyze}
  disabled={loading}
  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-medium px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
>
  {loading && (
    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
  )}
  {loading ? 'Analyzing...' : 'Analyze'}
</button>
        </div>

        {/* Error Message */}
        {errorMessage && (
          <div className="bg-red-950 border border-red-800 text-red-300 rounded-lg px-4 py-3 mb-6">
            {errorMessage}
          </div>
        )}

        {/* Result */}
        {result !== null && (
          <div className="space-y-8 mb-10">
            <div className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-3">
              <span className="text-gray-400">Total commits analyzed: </span>
              <span className="text-white font-semibold">{result.total_commits}</span>
            </div>

            <div>
              <h2 className="text-xl font-semibold text-white mb-3">🔥 Hotspot Files</h2>
              <div className="space-y-2">
                {result.hotspots.map((file) => (
                  <div
                    key={file.file_path}
                    className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 flex justify-between items-center"
                  >
                    <span className="text-gray-300 font-mono text-sm">{file.file_path}</span>
                    <span className="text-gray-500 text-sm">{file.change_count} changes</span>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h2 className="text-xl font-semibold text-white mb-3">⚠️ Bus Factor Risks</h2>
              <div className="space-y-2">
                {result.bus_factor_risks.map((risk) => (
                  <div
                    key={risk.file_path}
                    className="bg-red-950 border border-red-900 rounded-lg px-4 py-3"
                  >
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-gray-200 font-mono text-sm">{risk.file_path}</span>
                      <span className="text-red-400 text-sm font-semibold">
                        {risk.ownership_percent}% owned
                      </span>
                    </div>
                    <p className="text-gray-500 text-xs">
                      Main owner: {risk.owner_name}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h2 className="text-xl font-semibold text-white mb-3">🔗 Temporally Coupled Files</h2>
              <div className="space-y-2">
                {result.coupled_files.map((pair, index) => (
                  <div
                    key={index}
                    className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-3"
                  >
                    <div className="flex items-center gap-2 text-sm">
                      <span className="text-gray-300 font-mono">{pair.file_a}</span>
                      <span className="text-gray-600">↔</span>
                      <span className="text-gray-300 font-mono">{pair.file_b}</span>
                    </div>
                    <p className="text-gray-500 text-xs mt-1">
                      Changed together {pair.co_change_count} times
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Recent Analyses (History) */}
<div>
  <h2 className="text-xl font-semibold text-white mb-3">📋 Recent Analyses</h2>
  {history.length === 0 ? (
    <div className="bg-gray-900 border border-dashed border-gray-800 rounded-lg px-4 py-8 text-center">
      <p className="text-gray-500 text-sm">
        No analyses yet — paste a GitHub repo URL above to get started.
      </p>
    </div>
  ) : (
    <div className="space-y-2">
      {history.map((item) => (
        <div
          key={item.id}
          onClick={() => fetchProjectDetails(item.id)}
          className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 flex justify-between items-center cursor-pointer hover:border-blue-600 transition-colors"
        >
          <span className="text-gray-300 font-mono text-sm">{item.repo_url}</span>
          <div className="flex items-center gap-3">
            <span
              className={`text-xs px-2 py-1 rounded ${
                item.status === 'completed'
                  ? 'bg-green-950 text-green-400'
                  : 'bg-red-950 text-red-400'
              }`}
            >
              {item.status}
            </span>
            <button
              onClick={(e) => handleDelete(item.id, e)}
              className="text-gray-600 hover:text-red-400 transition-colors"
            >
              ✕
            </button>
          </div>
        </div>
      ))}
    </div>
  )}
</div>
      </div>
    </div>
  )
}

export default Dashboard