import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AuthPage from './pages/AuthPage'
import BrowsePage from './pages/BrowsePage'
import HistoryPage from './pages/HistoryPage'
import AgentPage from './pages/AgentPage'
import ProfilePage from './pages/ProfilePage'
import NavBar from './components/NavBar'

function PrivateRoute({ children }) {
  return localStorage.getItem('token') ? children : <Navigate to="/" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route
          path="/browse"
          element={
            <PrivateRoute>
              <NavBar />
              <BrowsePage />
            </PrivateRoute>
          }
        />
        <Route
          path="/history"
          element={
            <PrivateRoute>
              <NavBar />
              <HistoryPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/agent"
          element={
            <PrivateRoute>
              <NavBar />
              <AgentPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <NavBar />
              <ProfilePage />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}
