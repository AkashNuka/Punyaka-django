import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { productsAPI, cartAPI } from '../services/api'
import { useAuth } from '../context/AuthContext'
import { useRouter } from 'next/router'

export default function Products() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [addingToCart, setAddingToCart] = useState<number | null>(null)
  const { user } = useAuth()
  const router = useRouter()

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      const response = await productsAPI.getAll()
      setProducts(response.data.results || response.data)
    } catch (error) {
      console.error('Error loading products:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddToCart = async (productId: number) => {
    if (!user) {
      router.push('/login')
      return
    }

    setAddingToCart(productId)
    try {
      await cartAPI.addItem({ product_id: productId, quantity: 1 })
      alert('Product added to cart!')
    } catch (error) {
      console.error('Error adding to cart:', error)
      alert('Failed to add product to cart')
    } finally {
      setAddingToCart(null)
    }
  }

  return (
    <Layout>
      <div>
        <h1 className="text-4xl font-bold mb-8">Shop Spiritual Products</h1>

        {loading ? (
          <p>Loading products...</p>
        ) : (
          <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
            {products.map((product: any) => (
              <div key={product.id} className="bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="h-48 bg-gradient-to-br from-orange-100 to-red-100 flex items-center justify-center">
                  <span className="text-6xl">🙏</span>
                </div>
                <div className="p-4">
                  <h3 className="font-bold mb-2">{product.name}</h3>
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">{product.description}</p>
                  
                  <div className="flex justify-between items-center mb-3">
                    <div>
                      {product.discount_price ? (
                        <>
                          <span className="text-lg font-bold text-green-600">
                            ₹{product.discount_price}
                          </span>
                          <span className="text-sm text-gray-500 line-through ml-2">
                            ₹{product.price}
                          </span>
                        </>
                      ) : (
                        <span className="text-lg font-bold">₹{product.price}</span>
                      )}
                    </div>
                  </div>

                  <div className="text-sm text-gray-600 mb-3">
                    Stock: {product.stock > 0 ? `${product.stock} available` : 'Out of stock'}
                  </div>

                  <button
                    onClick={() => handleAddToCart(product.id)}
                    disabled={!product.is_in_stock || addingToCart === product.id}
                    className="w-full bg-orange-500 text-white py-2 rounded hover:bg-orange-600 disabled:bg-gray-400"
                  >
                    {addingToCart === product.id ? 'Adding...' : 'Add to Cart'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && products.length === 0 && (
          <p className="text-center text-gray-600">No products available at the moment.</p>
        )}
      </div>
    </Layout>
  )
}
