import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Layout from '../components/Layout'
import { useAuth } from '../context/AuthContext'
import { bookingsAPI, ordersAPI, getAdminUrl } from '../services/api'
import Link from 'next/link'

export default function Dashboard() {
  const { user, loading: authLoading } = useAuth()
  const router = useRouter()
  const [bookings, setBookings] = useState([])
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login')
    } else if (user) {
      loadData()
    }
  }, [user, authLoading])

  const loadData = async () => {
    try {
      const [bookingsRes, ordersRes] = await Promise.all([
        bookingsAPI.getAll(),
        ordersAPI.getAll()
      ])
      setBookings(bookingsRes.data.results || bookingsRes.data)
      setOrders(ordersRes.data.results || ordersRes.data)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (authLoading || loading) {
    return <Layout><p>Loading...</p></Layout>
  }

  if (!user) {
    return null
  }

  return (
    <Layout>
      <div>
        <h1 className="text-4xl font-bold mb-2">Welcome, {user.first_name}!</h1>
        <p className="text-gray-600 mb-8">Role: {user.role}</p>

        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-4">My Bookings</h2>
            {bookings.length > 0 ? (
              <div className="space-y-4">
                {bookings.map((booking: any) => (
                  <div key={booking.id} className="border-b pb-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-bold">{booking.service_details?.name || 'Service'}</p>
                        <p className="text-sm text-gray-600">
                          {booking.booking_date} at {booking.booking_time}
                        </p>
                        <p className="text-sm text-gray-600">
                          Status: <span className="font-semibold">{booking.status}</span>
                        </p>
                      </div>
                      <span className="text-lg font-bold">₹{booking.service_price}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No bookings yet</p>
                <Link
                  href="/priests"
                  className="inline-block bg-orange-500 text-white px-6 py-2 rounded hover:bg-orange-600"
                >
                  Book a Priest
                </Link>
              </div>
            )}
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-4">My Orders</h2>
            {orders.length > 0 ? (
              <div className="space-y-4">
                {orders.map((order: any) => (
                  <div key={order.id} className="border-b pb-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-bold">Order #{order.order_number}</p>
                        <p className="text-sm text-gray-600">
                          {order.items?.length || 0} item(s)
                        </p>
                        <p className="text-sm text-gray-600">
                          Status: <span className="font-semibold">{order.status}</span>
                        </p>
                      </div>
                      <span className="text-lg font-bold">₹{order.total_amount}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No orders yet</p>
                <Link
                  href="/products"
                  className="inline-block bg-orange-500 text-white px-6 py-2 rounded hover:bg-orange-600"
                >
                  Shop Products
                </Link>
              </div>
            )}
          </div>
        </div>

        {user.role === 'admin' && (
          <div className="mt-8 bg-blue-100 p-6 rounded-lg">
            <h2 className="text-2xl font-bold mb-4">Admin Access</h2>
            <p className="mb-4">Access the Django admin panel for full control:</p>
            <p className="mb-2 text-sm"><strong>Username:</strong> admin@punyaka.com</p>
            <p className="mb-4 text-sm"><strong>Password:</strong> admin123</p>
            <a
              href={getAdminUrl()}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600"
            >
              Open Admin Panel
            </a>
          </div>
        )}
      </div>
    </Layout>
  )
}
