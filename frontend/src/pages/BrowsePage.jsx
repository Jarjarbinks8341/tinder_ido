import { useState, useEffect } from 'react'
import { api } from '../api'
import CandidateCard from '../components/CandidateCard'

const GENDERS = [
  { value: '', label: 'Any' },
  { value: 'female', label: 'Women' },
  { value: 'male', label: 'Men' },
  { value: 'other', label: 'Other' },
]

export default function BrowsePage() {
  const [candidates, setCandidates] = useState([])
  const [index, setIndex] = useState(0)
  const [swiping, setSwiping] = useState(false)
  const [toast, setToast] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Filters
  const [gender, setGender] = useState('')
  const [minAge, setMinAge] = useState('')
  const [maxAge, setMaxAge] = useState('')
  const [tagInput, setTagInput] = useState('')

  async function search() {
    setLoading(true)
    setError('')
    setIndex(0)
    try {
      const filters = {}
      if (gender) filters.gender = gender
      if (minAge) filters.min_age = Number(minAge)
      if (maxAge) filters.max_age = Number(maxAge)
      if (tagInput.trim()) filters.tags = tagInput.split(',').map((t) => t.trim()).filter(Boolean)
      const results = await api.searchCandidates(filters)
      setCandidates(results)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { search() }, []) // eslint-disable-line react-hooks/exhaustive-deps

  async function handleSwipe(direction) {
    const candidate = candidates[index]
    setSwiping(true)
    try {
      await api.swipe(candidate.id, direction)
      const msg = direction === 'right'
        ? `❤️ Liked ${candidate.name}! Your agent will follow up.`
        : `👋 Passed on ${candidate.name}`
      showToast(msg, direction === 'right' ? 'green' : 'gray')
      setIndex((i) => i + 1)
    } catch (err) {
      showToast(err.message, 'red')
    } finally {
      setSwiping(false)
    }
  }

  function showToast(msg, color) {
    setToast({ msg, color })
    setTimeout(() => setToast(null), 2500)
  }

  const current = candidates[index]
  const remaining = candidates.length - index

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-lg mx-auto px-4 py-6 space-y-6">

        {/* Filters */}
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-3">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Filters</h2>
          <div className="flex flex-wrap gap-2">
            {GENDERS.map((g) => (
              <button
                key={g.value}
                onClick={() => setGender(g.value)}
                className={`px-3 py-1 rounded-full text-sm font-medium border transition-colors ${
                  gender === g.value
                    ? 'bg-rose-500 text-white border-rose-500'
                    : 'text-gray-500 border-gray-200 hover:border-rose-300'
                }`}
              >
                {g.label}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              className="w-24 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200"
              placeholder="Min age"
              type="number"
              min={18}
              max={100}
              value={minAge}
              onChange={(e) => setMinAge(e.target.value)}
            />
            <input
              className="w-24 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200"
              placeholder="Max age"
              type="number"
              min={18}
              max={100}
              value={maxAge}
              onChange={(e) => setMaxAge(e.target.value)}
            />
            <input
              className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200"
              placeholder="Tags: hiking, coffee…"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
            />
          </div>
          <button
            onClick={search}
            className="w-full bg-rose-500 hover:bg-rose-600 text-white text-sm font-semibold py-2 rounded-xl transition-colors"
          >
            Search
          </button>
        </div>

        {/* Card area */}
        <div className="flex flex-col items-center gap-4">
          {loading ? (
            <p className="text-gray-400 py-20">Loading…</p>
          ) : error ? (
            <p className="text-red-500 py-20">{error}</p>
          ) : !current ? (
            <div className="text-center py-20 space-y-2">
              <p className="text-4xl">🎉</p>
              <p className="text-gray-500 font-medium">
                {candidates.length === 0 ? 'No results. Try different filters.' : 'You\'ve seen everyone!'}
              </p>
              <button onClick={search} className="text-rose-500 text-sm hover:underline">
                Search again
              </button>
            </div>
          ) : (
            <>
              <p className="text-sm text-gray-400">{remaining} profile{remaining !== 1 ? 's' : ''} remaining</p>
              <CandidateCard candidate={current} onSwipe={handleSwipe} swiping={swiping} />
            </>
          )}
        </div>
      </div>

      {/* Toast */}
      {toast && (
        <div
          className={`fixed bottom-6 left-1/2 -translate-x-1/2 px-5 py-3 rounded-2xl text-white text-sm font-medium shadow-lg transition-all ${
            toast.color === 'green' ? 'bg-green-500' :
            toast.color === 'red'   ? 'bg-red-500'   : 'bg-gray-500'
          }`}
        >
          {toast.msg}
        </div>
      )}
    </div>
  )
}
