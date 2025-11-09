import Link from 'next/link'
import { useAuth } from '../context/AuthContext'
import { useRouter } from 'next/router'

export default function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth()
  const router = useRouter()

  const handleLogout = async () => {
    try {
      await logout()
      router.push('/login')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="bg-gradient-to-r from-orange-500 to-red-600 text-white shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="text-2xl font-bold flex items-center">
              🕉️ Punyaka
            </Link>
            
            <div className="flex items-center space-x-6">
              <Link href="/priests" className="hover:text-orange-200">
                Find Priests
              </Link>
              <Link href="/products" className="hover:text-orange-200">
                Shop
              </Link>
              {user && (
                <Link href="/cart" className="hover:text-orange-200">
                  🛒 Cart
                </Link>
              )}
              
              {user ? (
                <>
                  <Link href="/dashboard" className="hover:text-orange-200">
                    Dashboard
                  </Link>
                  <span className="text-sm">
                    {user.first_name || user.username} ({user.role})
                  </span>
                  <button
                    onClick={handleLogout}
                    className="bg-white text-orange-600 px-4 py-2 rounded hover:bg-orange-100"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    href="/login"
                    className="hover:text-orange-200"
                  >
                    Login
                  </Link>
                  <Link
                    href="/register"
                    className="bg-white text-orange-600 px-4 py-2 rounded hover:bg-orange-100"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-grow container mx-auto px-4 py-8">
        {children}
      </main>

      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p>© 2024 Punyaka - Spiritual Services Platform</p>
          <p className="text-sm text-gray-400 mt-2">
            Connecting devotees with authentic spiritual services
          </p>
        </div>
      </footer>
    </div>
  )
}
