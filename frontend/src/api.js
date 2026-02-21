const BASE = import.meta.env.VITE_API_BASE || '/api'

function getToken() {
  return localStorage.getItem('token')
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${getToken()}`,
  }
}

async function request(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: authHeaders(),
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Request failed')
  }
  return res.json()
}

export const api = {
  register: (data) =>
    fetch(`${BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(async (r) => {
      if (!r.ok) throw new Error((await r.json()).detail)
      return r.json()
    }),

  login: (email, password) =>
    fetch(`${BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    }).then(async (r) => {
      if (!r.ok) throw new Error((await r.json()).detail)
      return r.json()
    }),

  getMe: () => request('GET', '/auth/me'),
  searchCandidates: (filters) => request('POST', '/candidates/search', filters),
  swipe: (candidateId, direction) =>
    request('POST', `/swipes/${candidateId}`, { direction }),
  getSwipeHistory: () => request('GET', '/swipes'),
  getMatches: () => request('GET', '/swipes/matches'),
  getAgent: () => request('GET', '/agent/me'),
  getMatchmakers: () => request('GET', '/matchmaker'),

  updateProfile: (data) => request('PATCH', '/users/me', data),

  uploadPhotos: (files) => {
    const formData = new FormData()
    for (const file of files) {
      formData.append('files', file)
    }
    return fetch(`${BASE}/users/me/photos`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${getToken()}` },
      body: formData,
    }).then(async (r) => {
      if (!r.ok) throw new Error((await r.json()).detail || 'Upload failed')
      return r.json()
    })
  },

  deletePhoto: (photoId) =>
    fetch(`${BASE}/users/me/photos/${photoId}`, {
      method: 'DELETE',
      headers: authHeaders(),
    }).then(async (r) => {
      if (!r.ok) throw new Error((await r.json()).detail || 'Delete failed')
      return r.json()
    }),
}
