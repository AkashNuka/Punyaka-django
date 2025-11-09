import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Layout from '../../components/Layout'
import { priestsAPI, servicesAPI, bookingsAPI } from '../../services/api'
import { useAuth } from '../../context/AuthContext'

export default function PriestDetail() {
  const router = useRouter()
  const { id } = router.query
  const { user } = useAuth()
  
  const [priest, setPriest] = useState<any>(null)
  const [services, setServices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [booking, setBooking] = useState({
    service_id: '',
    booking_date: '',
    booking_time: '',
    location: '',
    special_requirements: ''
  })
  const [bookingLoading, setBookingLoading] = useState(false)

  useEffect(() => {
    if (id) {
      loadPriestData()
      loadServices()
    }
  }, [id])

  const loadPriestData = async () => {
    try {
      const response = await priestsAPI.getById(Number(id))
      setPriest(response.data)
    } catch (error) {
      console.error('Error loading priest:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadServices = async () => {
    try {
      const response = await servicesAPI.getAll()
      setServices(response.data.results || response.data)
    } catch (error) {
      console.error('Error loading services:', error)
    }
  }

  const handleBooking = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!user) {
      alert('Please login to book a priest')
      router.push('/login')
      return
    }

    setBookingLoading(true)
    try {
      await bookingsAPI.create({
        ...booking,
        priest_id: Number(id),
        service_id: Number(booking.service_id)
      })
      alert('Booking request submitted successfully! The priest will contact you soon.')
      router.push('/dashboard')
    } catch (error: any) {
      console.error('Error creating booking:', error)
      alert(error.response?.data?.message || 'Failed to create booking. Please try again.')
    } finally {
      setBookingLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="text-center py-12">Loading priest details...</div>
      </Layout>
    )
  }

  if (!priest) {
    return (
      <Layout>
        <div className="text-center py-12">Priest not found</div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        {/* Priest Profile */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold mb-2">
                {priest.user.first_name} {priest.user.last_name}
              </h1>
              <div className="text-yellow-500 text-xl mb-2">
                ⭐ {priest.average_rating} ({priest.total_ratings} reviews)
              </div>
              <p className="text-gray-600">
                {priest.experience_years} years of experience
              </p>
            </div>
            {priest.is_verified && (
              <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full font-semibold">
                ✓ Verified
              </div>
            )}
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="font-bold text-lg mb-2">Specializations</h3>
              <div className="flex flex-wrap gap-2">
                {priest.specializations_list?.map((spec: string, index: number) => (
                  <span key={index} className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm">
                    {spec}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-bold text-lg mb-2">Languages</h3>
              <div className="flex flex-wrap gap-2">
                {priest.languages_list?.map((lang: string, index: number) => (
                  <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                    {lang}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="border-t pt-4">
            <p className="text-gray-600">
              <strong>Service Radius:</strong> {priest.service_radius_km} km
            </p>
            <p className="text-gray-600">
              <strong>Contact:</strong> {priest.user.phone}
            </p>
          </div>
        </div>

        {/* Booking Form */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Book a Service</h2>

          <form onSubmit={handleBooking} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Select Service *
              </label>
              <select
                required
                value={booking.service_id}
                onChange={(e) => setBooking({ ...booking, service_id: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500"
              >
                <option value="">Choose a service...</option>
                {services.map((service) => (
                  <option key={service.id} value={service.id}>
                    {service.name} - ₹{service.price}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Preferred Date *
                </label>
                <input
                  type="date"
                  required
                  value={booking.booking_date}
                  onChange={(e) => setBooking({ ...booking, booking_date: e.target.value })}
                  min={new Date().toISOString().split('T')[0]}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Preferred Time *
                </label>
                <input
                  type="time"
                  required
                  value={booking.booking_time}
                  onChange={(e) => setBooking({ ...booking, booking_time: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Location / Address *
              </label>
              <textarea
                required
                value={booking.location}
                onChange={(e) => setBooking({ ...booking, location: e.target.value })}
                rows={3}
                placeholder="Enter the full address where the service should be performed"
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Special Requirements (Optional)
              </label>
              <textarea
                value={booking.special_requirements}
                onChange={(e) => setBooking({ ...booking, special_requirements: e.target.value })}
                rows={3}
                placeholder="Any specific requirements or instructions..."
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500"
              />
            </div>

            <div className="flex gap-4">
              <button
                type="submit"
                disabled={bookingLoading}
                className="flex-1 bg-orange-500 text-white py-3 rounded-lg hover:bg-orange-600 font-semibold disabled:bg-gray-400"
              >
                {bookingLoading ? 'Submitting...' : 'Submit Booking Request'}
              </button>
              <button
                type="button"
                onClick={() => router.back()}
                className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
            </div>
          </form>

          <p className="text-sm text-gray-600 mt-4">
            * After submitting, the priest will review your request and contact you to confirm the booking details and payment.
          </p>
        </div>
      </div>
    </Layout>
  )
}
