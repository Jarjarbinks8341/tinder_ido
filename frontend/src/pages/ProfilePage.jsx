import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'

export default function ProfilePage() {
  const navigate = useNavigate()
  const fileInputRef = useRef(null)

  const [user, setUser] = useState(null)
  const [form, setForm] = useState({ location: '', bio: '', tags: '' })
  const [saving, setSaving] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    api.getMe().then((me) => {
      setUser(me)
      setForm({
        location: me.location || '',
        bio: me.bio || '',
        tags: me.tags || '',
      })
    })
  }, [])

  function set(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  async function saveProfile(e) {
    e.preventDefault()
    setError('')
    setSuccess('')
    setSaving(true)
    try {
      const updated = await api.updateProfile({
        location: form.location || null,
        bio: form.bio || null,
        tags: form.tags || null,
      })
      setUser(updated)
      setSuccess('Profile saved!')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  async function handlePhotoUpload(e) {
    const files = Array.from(e.target.files)
    if (!files.length) return
    setError('')
    setUploading(true)
    try {
      const updated = await api.uploadPhotos(files)
      setUser(updated)
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  async function handleDeletePhoto(photoId) {
    setError('')
    try {
      const updated = await api.deletePhoto(photoId)
      setUser(updated)
    } catch (err) {
      setError(err.message)
    }
  }

  const inputClass =
    'w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-300'

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <p className="text-gray-400">Loading…</p>
      </div>
    )
  }

  const photoCount = user.photos?.length ?? 0

  return (
    <div className="max-w-lg mx-auto px-4 py-8 space-y-8">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-800">Your Profile</h1>
        <p className="text-gray-400 text-sm mt-1">{user.name} · {user.gender} · {user.age}</p>
      </div>

      {/* Text info */}
      <section className="bg-white rounded-2xl shadow-sm p-6 space-y-4">
        <h2 className="font-semibold text-gray-700">About You</h2>
        <form onSubmit={saveProfile} className="space-y-3">
          <input
            className={inputClass}
            placeholder="Location (e.g. San Francisco, CA)"
            value={form.location}
            onChange={set('location')}
          />
          <textarea
            className={inputClass}
            placeholder="Bio — tell people about yourself"
            rows={3}
            value={form.bio}
            onChange={set('bio')}
          />
          <input
            className={inputClass}
            placeholder="Interests, comma-separated (e.g. hiking,coffee,music)"
            value={form.tags}
            onChange={set('tags')}
          />
          {success && <p className="text-green-500 text-sm">{success}</p>}
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={saving}
            className="w-full bg-rose-500 hover:bg-rose-600 text-white font-semibold py-2.5 rounded-xl transition-colors disabled:opacity-50"
          >
            {saving ? 'Saving…' : 'Save'}
          </button>
        </form>
      </section>

      {/* Photos */}
      <section className="bg-white rounded-2xl shadow-sm p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold text-gray-700">Photos ({photoCount}/6)</h2>
          {photoCount < 6 && (
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="text-sm text-rose-500 hover:text-rose-600 font-medium disabled:opacity-50"
            >
              {uploading ? 'Uploading…' : '+ Add photos'}
            </button>
          )}
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          className="hidden"
          onChange={handlePhotoUpload}
        />

        {photoCount === 0 ? (
          <div
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-gray-200 rounded-xl p-8 text-center cursor-pointer hover:border-rose-300 transition-colors"
          >
            <p className="text-gray-400 text-sm">Click to upload your first photo</p>
          </div>
        ) : (
          <div className="grid grid-cols-3 gap-3">
            {user.photos.map((photo) => (
              <div key={photo.id} style={{ position: 'relative', aspectRatio: '1/1' }}>
                <img
                  src={photo.url}
                  alt="profile"
                  style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '12px', display: 'block' }}
                />
                <button
                  onClick={() => handleDeletePhoto(photo.id)}
                  style={{
                    position: 'absolute', top: '4px', right: '4px', zIndex: 50,
                    width: '24px', height: '24px', borderRadius: '50%',
                    background: 'rgba(0,0,0,0.65)', color: 'white',
                    border: 'none', cursor: 'pointer', fontSize: '16px',
                    lineHeight: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
                  }}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      <button
        onClick={() => navigate('/browse')}
        className="w-full border border-rose-300 text-rose-500 hover:bg-rose-50 font-semibold py-2.5 rounded-xl transition-colors"
      >
        Continue to Browse
      </button>
    </div>
  )
}
