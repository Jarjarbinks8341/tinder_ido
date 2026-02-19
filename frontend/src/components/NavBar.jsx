import { NavLink, useNavigate } from 'react-router-dom'

export default function NavBar() {
  const navigate = useNavigate()

  function logout() {
    localStorage.removeItem('token')
    navigate('/')
  }

  const linkClass = ({ isActive }) =>
    `px-3 py-1 rounded-full text-sm font-medium transition-colors ${
      isActive
        ? 'bg-rose-500 text-white'
        : 'text-gray-600 hover:text-rose-500'
    }`

  return (
    <nav className="flex items-center justify-between px-6 py-3 bg-white border-b border-gray-100 shadow-sm">
      <span className="text-rose-500 font-bold text-xl tracking-tight">
        Tinder IDO
      </span>
      <div className="flex items-center gap-2">
        <NavLink to="/browse" className={linkClass}>Browse</NavLink>
        <NavLink to="/history" className={linkClass}>History</NavLink>
        <NavLink to="/agent" className={linkClass}>Agent</NavLink>
        <button
          onClick={logout}
          className="ml-4 px-3 py-1 text-sm text-gray-500 hover:text-red-500 transition-colors"
        >
          Logout
        </button>
      </div>
    </nav>
  )
}
