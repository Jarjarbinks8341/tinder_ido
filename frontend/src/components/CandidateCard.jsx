const EDUCATION_LABELS = {
  high_school: 'High School',
  associate: 'Associate',
  bachelor: "Bachelor's",
  master: "Master's",
  phd: 'PhD',
  other: 'Other',
}

const INDUSTRY_LABELS = {
  engineering: 'Engineering',
  education: 'Education',
  financial_services: 'Financial Services',
  healthcare: 'Healthcare',
  legal: 'Legal',
  marketing: 'Marketing',
  real_estate: 'Real Estate',
  technology: 'Technology',
  hospitality: 'Hospitality',
  government: 'Government',
  arts_entertainment: 'Arts & Entertainment',
  other: 'Other',
}

export default function CandidateCard({ candidate, onSwipe, swiping }) {
  const tags = candidate.tags ? candidate.tags.split(',') : []

  return (
    <div className="w-80 bg-white rounded-3xl shadow-xl overflow-hidden select-none">
      {/* Photo */}
      <div className="relative h-96 bg-gray-100">
        {candidate.photo_url ? (
          <img
            src={candidate.photo_url}
            alt={candidate.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-6xl text-gray-300">
            👤
          </div>
        )}
        {/* Gradient overlay */}
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black/60 to-transparent" />
        <div className="absolute bottom-4 left-4 text-white">
          <p className="text-2xl font-bold">
            {candidate.name}, {candidate.age}
          </p>
          {candidate.location && (
            <p className="text-sm opacity-90">📍 {candidate.location}</p>
          )}
        </div>
      </div>

      {/* Info */}
      <div className="p-4 space-y-3">
        {candidate.bio && (
          <p className="text-gray-600 text-sm leading-relaxed">{candidate.bio}</p>
        )}
        {(candidate.education || candidate.industry || candidate.income_range) && (
          <div className="flex flex-wrap gap-2 text-xs text-gray-500">
            {candidate.education && (
              <span className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full">
                {EDUCATION_LABELS[candidate.education] || candidate.education}
              </span>
            )}
            {candidate.industry && (
              <span className="px-2 py-0.5 bg-purple-50 text-purple-600 rounded-full">
                {INDUSTRY_LABELS[candidate.industry] || candidate.industry}
              </span>
            )}
            {candidate.income_range && candidate.income_range !== 'prefer_not_to_say' && (
              <span className="px-2 py-0.5 bg-green-50 text-green-600 rounded-full">
                ${candidate.income_range}
              </span>
            )}
          </div>
        )}
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 bg-rose-50 text-rose-500 text-xs rounded-full font-medium"
              >
                {tag.trim()}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Swipe buttons */}
      <div className="flex justify-center gap-8 pb-5">
        <button
          onClick={() => onSwipe('left')}
          disabled={swiping}
          className="w-14 h-14 rounded-full border-2 border-gray-200 flex items-center justify-center text-2xl
                     hover:border-red-400 hover:bg-red-50 transition-colors disabled:opacity-40"
          title="Pass"
        >
          ✕
        </button>
        <button
          onClick={() => onSwipe('right')}
          disabled={swiping}
          className="w-14 h-14 rounded-full border-2 border-gray-200 flex items-center justify-center text-2xl
                     hover:border-green-400 hover:bg-green-50 transition-colors disabled:opacity-40"
          title="Like"
        >
          ♥
        </button>
      </div>
    </div>
  )
}
