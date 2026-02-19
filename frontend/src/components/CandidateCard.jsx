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
