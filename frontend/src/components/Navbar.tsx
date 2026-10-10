import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function Navbar() {
  const { user, token, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="border-b border-gray-800 bg-gray-950">
      <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">

        <div className="flex items-center gap-6">
  <Link to={token ? '/dashboard' : '/login'} className="text-xl font-bold text-white">
    OnboardGit
  </Link>
  <Link to="/about" className="text-gray-400 hover:text-white text-sm transition-colors">
    About
  </Link>
</div>

        {token && (
          <div className="flex items-center gap-4">
            <span className="text-gray-400 text-sm">{user?.username}</span>
            <button
              onClick={handleLogout}
              className="text-sm text-gray-500 hover:text-red-400 transition-colors"
            >
              Log out
            </button>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar