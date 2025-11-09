import { useEffect } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'

export default function Home() {
  const { user } = useAuth()
  const router = useRouter()

  return (
    <Layout>
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-800 mb-6">
          Welcome to Punyaka 🕉️
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Your trusted platform for authentic spiritual services, priest bookings,
          and sacred items
        </p>

        <div className="grid md:grid-cols-3 gap-8 mt-12">
          <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
            <div className="text-4xl mb-4">🙏</div>
            <h3 className="text-2xl font-bold mb-4">Book Priests</h3>
            <p className="text-gray-600 mb-4">
              Connect with verified priests for poojas, homas, and ceremonies at your location
            </p>
            <Link
              href="/priests"
              className="inline-block bg-orange-500 text-white px-6 py-2 rounded hover:bg-orange-600"
            >
              Find Priests
            </Link>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
            <div className="text-4xl mb-4">🛍️</div>
            <h3 className="text-2xl font-bold mb-4">Shop Samagri</h3>
            <p className="text-gray-600 mb-4">
              Browse our collection of authentic pooja items, idols, and spiritual gifts
            </p>
            <Link
              href="/products"
              className="inline-block bg-orange-500 text-white px-6 py-2 rounded hover:bg-orange-600"
            >
              Browse Products
            </Link>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
            <div className="text-4xl mb-4">📖</div>
            <h3 className="text-2xl font-bold mb-4">Your Orders</h3>
            <p className="text-gray-600 mb-4">
              View your bookings, orders, and track your spiritual journey with us
            </p>
            <Link
              href={user ? "/dashboard" : "/login"}
              className="inline-block bg-orange-500 text-white px-6 py-2 rounded hover:bg-orange-600"
            >
              {user ? "Go to Dashboard" : "Login to Continue"}
            </Link>
          </div>
        </div>

        {!user && (
          <div className="mt-12 bg-gradient-to-r from-orange-100 to-red-100 p-8 rounded-lg">
            <h3 className="text-2xl font-bold mb-4">New to Punyaka?</h3>
            <p className="text-gray-700 mb-4">
              Join thousands of devotees who trust us for their spiritual needs
            </p>
            <Link
              href="/register"
              className="inline-block bg-orange-500 text-white px-8 py-3 rounded-lg hover:bg-orange-600 font-bold"
            >
              Create Free Account
            </Link>
          </div>
        )}
      </div>
    </Layout>
  )
}
