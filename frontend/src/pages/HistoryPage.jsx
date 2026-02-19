import { useState, useEffect } from 'react'
import { api } from '../api'

export default function HistoryPage() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all') // 'all' | 'right' | 'left'

  useEffect(() => {
    api.getSwipeHistory()
      .then(setHistory)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const filtered = history.filter((s) => filter === 'all' || s.direction === filter)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">Swipe History</h1>
          <div className="flex gap-1">
            {['all', 'right', 'left'].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-1 rounded-full text-xs font-semibold capitalize transition-colors ${
                  filter === f
                    ? 'bg-rose-500 text-white'
                    : 'text-gray-500 bg-white border border-gray-200 hover:border-rose-300'
                }`}
              >
                {f === 'right' ? '❤️ Liked' : f === 'left' ? '✕ Passed' : 'All'}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <p className="text-center text-gray-400 py-20">Loading…</p>
        ) : filtered.length === 0 ? (
          <p className="text-center text-gray-400 py-20">No swipes yet.</p>
        ) : (
          <div className="space-y-2">
            {filtered.map((swipe) => {
              const liked = swipe.direction === 'right'
              return (
                <div
                  key={swipe.id}
                  className="flex items-center gap-4 bg-white rounded-2xl p-3 shadow-sm"
                >
                  <img
                    src={swipe.candidate.photo_url || 'https://via.placeholder.com/48'}
                    alt={swipe.candidate.name}
                    className="w-12 h-12 rounded-full object-cover"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-gray-800 truncate">
                      {swipe.candidate.name}, {swipe.candidate.age}
                    </p>
                    <p className="text-xs text-gray-400 truncate">
                      {swipe.candidate.tags?.split(',').join(' · ')}
                    </p>
                  </div>
                  <span
                    className={`text-xs font-bold px-2 py-1 rounded-full ${
                      liked
                        ? 'bg-green-100 text-green-600'
                        : 'bg-gray-100 text-gray-500'
                    }`}
                  >
                    {liked ? '❤️ Liked' : '✕ Passed'}
                  </span>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
