import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'

export default function AuthPage() {
  const navigate = useNavigate()
  const [mode, setMode] = useState('login') // 'login' | 'register'
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const [form, setForm] = useState({
    email: '', password: '', name: '', gender: 'male', age: '',
    location: '', bio: '', tags: '',
  })

  function set(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  async function submit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const isRegister = mode === 'register'
      if (isRegister) {
        const payload = { ...form, age: Number(form.age) }
        if (!payload.location) delete payload.location
        if (!payload.bio) delete payload.bio
        if (!payload.tags) delete payload.tags
        await api.register(payload)
      }
      const { access_token } = await api.login(form.email, form.password)
      localStorage.setItem('token', access_token)
      const me = await api.getMe()
      localStorage.setItem('gender', me.gender)
      navigate(isRegister ? '/profile' : '/browse')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const inputClass =
    'w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-rose-300'

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 to-pink-100 flex items-center justify-center p-4">
      <div className="w-full max-w-sm bg-white rounded-3xl shadow-xl p-8 space-y-6">
        {/* Header */}
        <div className="text-center space-y-1">
          <h1 className="text-3xl font-bold text-rose-500">Tinder IDO</h1>
          <p className="text-gray-400 text-sm">
            {mode === 'login' ? 'Welcome back' : 'Create your account'}
          </p>
        </div>

        {/* Form */}
        <form onSubmit={submit} className="space-y-3">
          {mode === 'register' && (
            <>
              <input
                className={inputClass}
                placeholder="Full name"
                value={form.name}
                onChange={set('name')}
                required
              />
              <div className="flex gap-2">
                <select
                  className={inputClass}
                  value={form.gender}
                  onChange={set('gender')}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
                <input
                  className={inputClass}
                  placeholder="Age"
                  type="number"
                  min={18}
                  max={100}
                  value={form.age}
                  onChange={set('age')}
                  required
                />
              </div>
              <input
                className={inputClass}
                placeholder="Location (optional)"
                value={form.location}
                onChange={set('location')}
              />
              <textarea
                className={inputClass}
                placeholder="Bio (optional)"
                rows={2}
                value={form.bio}
                onChange={set('bio')}
              />
              <input
                className={inputClass}
                placeholder="Interests, comma-separated (optional)"
                value={form.tags}
                onChange={set('tags')}
              />
            </>
          )}
          <input
            className={inputClass}
            placeholder="Email"
            type="email"
            value={form.email}
            onChange={set('email')}
            required
          />
          <input
            className={inputClass}
            placeholder="Password"
            type="password"
            value={form.password}
            onChange={set('password')}
            required
          />

          {error && (
            <p className="text-red-500 text-sm text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-rose-500 hover:bg-rose-600 text-white font-semibold py-2.5 rounded-xl transition-colors disabled:opacity-50"
          >
            {loading ? 'Please wait…' : mode === 'login' ? 'Log in' : 'Create account'}
          </button>
        </form>

        {/* Toggle */}
        <p className="text-center text-sm text-gray-400">
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <button
            onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}
            className="text-rose-500 font-medium hover:underline"
          >
            {mode === 'login' ? 'Sign up' : 'Log in'}
          </button>
        </p>
      </div>
    </div>
  )
}
