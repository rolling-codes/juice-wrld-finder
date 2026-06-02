import { Link } from 'react-router-dom'
import Router from './router'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <nav className="bg-black border-b border-gray-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="text-2xl font-bold">
              Juice WRLD Finder
            </Link>
            <Link
              to="/admin/login"
              className="text-sm text-gray-300 hover:text-white transition"
            >
              Admin
            </Link>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Router />
      </main>
    </div>
  )
}
