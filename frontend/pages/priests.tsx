import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { priestsAPI } from '../services/api'
import Link from 'next/link'

export default function Priests() {
  const [priests, setPriests] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPriests()
  }, [])

  const loadPriests = async () => {
    try {
      const response = await priestsAPI.getAll()
      setPriests(response.data.results || response.data)
    } catch (error) {
      console.error('Error loading priests:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div>
        <h1 className="text-4xl font-bold mb-8">Find Verified Priests</h1>

        {loading ? (
          <p>Loading priests...</p>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {priests.map((priest: any) => (
              <div key={priest.id} className="bg-white p-6 rounded-lg shadow-lg">
                <h3 className="text-xl font-bold mb-2">
                  {priest.user.first_name} {priest.user.last_name}
                </h3>
                <div className="text-yellow-500 mb-2">
                  ⭐ {priest.average_rating} ({priest.total_ratings} reviews)
                </div>
                <p className="text-gray-600 text-sm mb-2">
                  {priest.experience_years} years experience
                </p>
                <p className="text-gray-700 mb-3">
                  <strong>Specializations:</strong> {priest.specializations}
                </p>
                <p className="text-gray-600 text-sm mb-4">
                  <strong>Languages:</strong> {priest.languages}
                </p>
                <Link
                  href={`/priests/${priest.id}`}
                  className="block w-full text-center bg-orange-500 text-white py-2 rounded hover:bg-orange-600"
                >
                  View Profile & Book
                </Link>
              </div>
            ))}
          </div>
        )}

        {!loading && priests.length === 0 && (
          <p className="text-center text-gray-600">No priests available at the moment.</p>
        )}
      </div>
    </Layout>
  )
}
