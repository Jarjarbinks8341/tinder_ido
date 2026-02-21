import { useState, useEffect } from 'react'
import { api } from '../api'

const STATUS_STYLES = {
  pending:   'bg-yellow-100 text-yellow-700',
  contacted: 'bg-blue-100 text-blue-700',
  matched:   'bg-green-100 text-green-700',
  rejected:  'bg-red-100 text-red-600',
  active:    'bg-green-100 text-green-700',
  inactive:  'bg-gray-100 text-gray-500',
}

export default function AgentPage() {
  const [agent, setAgent] = useState(null)
  const [matchmakers, setMatchmakers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([api.getAgent(), api.getMatchmakers()])
      .then(([a, mm]) => { setAgent(a); setMatchmakers(mm) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-400">Loading…</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-lg mx-auto px-4 py-6 space-y-6">

        {/* Agent card */}
        {agent && (
          <div className="bg-white rounded-2xl shadow-sm p-5 space-y-2">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-gray-800">{agent.name}</h2>
                <p className="text-xs text-gray-400">Your personal matchmaking agent</p>
              </div>
              <span className={`text-xs font-semibold px-3 py-1 rounded-full capitalize ${STATUS_STYLES[agent.status] ?? 'bg-gray-100 text-gray-500'}`}>
                {agent.status}
              </span>
            </div>
            {agent.notes ? (
              <p className="text-sm text-gray-500">{agent.notes}</p>
            ) : (
              <p className="text-sm text-gray-400 italic">
                Agent is standing by — will reach out to your matches on your behalf.
              </p>
            )}
          </div>
        )}

        {/* Matchmaker records */}
        <div className="space-y-3">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">
            Matchmaker Pipeline ({matchmakers.length})
          </h2>

          {matchmakers.length === 0 ? (
            <div className="text-center py-16 space-y-2">
              <p className="text-3xl">💌</p>
              <p className="text-gray-400 text-sm">
                No matches yet. Swipe right on someone you like!
              </p>
            </div>
          ) : (
            matchmakers.map((mm) => (
              <div
                key={mm.id}
                className="flex items-center gap-4 bg-white rounded-2xl p-3 shadow-sm"
              >
                <img
                  src={mm.target_user.photo_url || 'https://via.placeholder.com/48'}
                  alt={mm.target_user.name}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-gray-800 truncate">
                    {mm.target_user.name}, {mm.target_user.age}
                  </p>
                  <p className="text-xs text-gray-400 truncate">
                    {mm.target_user.location}
                  </p>
                  {mm.contact_notes && (
                    <p className="text-xs text-gray-500 mt-0.5 italic">{mm.contact_notes}</p>
                  )}
                </div>
                <span className={`text-xs font-semibold px-2 py-1 rounded-full capitalize whitespace-nowrap ${STATUS_STYLES[mm.status] ?? 'bg-gray-100 text-gray-500'}`}>
                  {mm.status}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
