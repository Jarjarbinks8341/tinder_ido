import { useState, useEffect } from 'react'
import { api } from '../api'
import CandidateCard from '../components/CandidateCard'

const OPPOSITE = { male: 'female', female: 'male', other: 'other' }

function getOppositeGender() {
  const myGender = localStorage.getItem('gender') || 'male'
  return OPPOSITE[myGender] ?? 'female'
}

export default function BrowsePage() {
  const oppositeGender = getOppositeGender()

  const [candidates, setCandidates] = useState([])
  const [index, setIndex] = useState(0)
  const [swiping, setSwiping] = useState(false)
  const [toast, setToast] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Filters — gender is fixed to opposite
  const [minAge, setMinAge] = useState('')
  const [maxAge, setMaxAge] = useState('')
  const [tagInput, setTagInput] = useState('')
  const [location, setLocation] = useState('')
  const [education, setEducation] = useState('')
  const [industry, setIndustry] = useState('')
  const [incomeRange, setIncomeRange] = useState('')

  async function search() {
    setLoading(true)
    setError('')
    setIndex(0)
    try {
      const filters = { gender: oppositeGender }
      if (minAge) filters.min_age = Number(minAge)
      if (maxAge) filters.max_age = Number(maxAge)
      if (tagInput.trim()) filters.tags = tagInput.split(',').map((t) => t.trim()).filter(Boolean)
      if (location.trim()) filters.location = location.trim()
      if (education) filters.education = education
      if (industry) filters.industry = industry
      if (incomeRange) filters.income_range = incomeRange
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
    } catch (err) {
      // Still advance — a failure usually means already swiped (stale card)
      showToast('Skipped — already swiped on this person', 'gray')
    } finally {
      setSwiping(false)
      setIndex((i) => i + 1)
    }
  }

  function showToast(msg, color) {
    setToast({ msg, color })
    setTimeout(() => setToast(null), 2500)
  }

  const current = candidates[index]
  const remaining = candidates.length - index
  const genderLabel = oppositeGender.charAt(0).toUpperCase() + oppositeGender.slice(1) + 's'

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-lg mx-auto px-4 py-6 space-y-6">

        {/* Filters */}
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Filters</h2>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-rose-50 text-rose-500">
              Showing: {genderLabel}
            </span>
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
            <select
              className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            >
              <option value="">Location</option>
              <option value="Sydney">Sydney</option>
              <option value="Melbourne">Melbourne</option>
              <option value="Brisbane">Brisbane</option>
              <option value="Perth">Perth</option>
              <option value="Adelaide">Adelaide</option>
              <option value="Gold Coast">Gold Coast</option>
              <option value="Canberra">Canberra</option>
              <option value="Hobart">Hobart</option>
              <option value="Darwin">Darwin</option>
            </select>
          </div>
          <div className="flex gap-2">
            <select
              className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200"
              value={education}
              onChange={(e) => setEducation(e.target.value)}
            >
              <option value="">Education</option>
              <option value="high_school">High School</option>
              <option value="associate">Associate</option>
              <option value="bachelor">Bachelor's</option>
              <option value="master">Master's</option>
              <option value="phd">PhD</option>
              <option value="other">Other</option>
            </select>
            <select
              className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200"
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
            >
              <option value="">Industry</option>
              <option value="engineering">Engineering</option>
              <option value="education">Education</option>
              <option value="financial_services">Financial Services</option>
              <option value="healthcare">Healthcare</option>
              <option value="legal">Legal</option>
              <option value="marketing">Marketing</option>
              <option value="real_estate">Real Estate</option>
              <option value="technology">Technology</option>
              <option value="hospitality">Hospitality</option>
              <option value="government">Government</option>
              <option value="arts_entertainment">Arts & Entertainment</option>
              <option value="other">Other</option>
            </select>
            <select
              className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200"
              value={incomeRange}
              onChange={(e) => setIncomeRange(e.target.value)}
            >
              <option value="">Income</option>
              <option value="0-50K">$0–50K</option>
              <option value="50K-100K">$50K–100K</option>
              <option value="100K-150K">$100K–150K</option>
              <option value="150K-200K">$150K–200K</option>
              <option value="200K+">$200K+</option>
            </select>
          </div>
          <input
            className="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200"
            placeholder="Interests: hiking, coffee…"
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
          />
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
                {candidates.length === 0 ? 'No results. Try different filters.' : "You've seen everyone!"}
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
