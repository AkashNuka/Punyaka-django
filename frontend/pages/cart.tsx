import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { cartAPI, ordersAPI } from '../services/api'
import { useAuth } from '../context/AuthContext'
import { useRouter } from 'next/router'
import Link from 'next/link'

export default function Cart() {
  const [cart, setCart] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [checkoutLoading, setCheckoutLoading] = useState(false)
  const { user } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!user) {
      router.push('/login')
      return
    }
    loadCart()
  }, [user])

  const loadCart = async () => {
    try {
      const response = await cartAPI.get()
      setCart(response.data)
    } catch (error) {
      console.error('Error loading cart:', error)
    } finally {
      setLoading(false)
    }
  }

  const updateQuantity = async (itemId: number, quantity: number) => {
    if (quantity < 1) return
    
    try {
      await cartAPI.updateItem(itemId, { quantity })
      loadCart()
    } catch (error) {
      console.error('Error updating quantity:', error)
      alert('Failed to update quantity')
    }
  }

  const removeItem = async (itemId: number) => {
    if (!confirm('Remove this item from cart?')) return
    
    try {
      await cartAPI.removeItem(itemId)
      loadCart()
    } catch (error) {
      console.error('Error removing item:', error)
      alert('Failed to remove item')
    }
  }

  const handleCheckout = async () => {
    if (!cart || cart.items.length === 0) return
    
    setCheckoutLoading(true)
    try {
      const response = await ordersAPI.create({
        cart_id: cart.id,
        shipping_address: 'Please update shipping address'
      })
      alert('Order placed successfully!')
      router.push('/dashboard')
    } catch (error: any) {
      console.error('Error creating order:', error)
      alert(error.response?.data?.message || 'Failed to place order')
    } finally {
      setCheckoutLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="text-center py-12">Loading cart...</div>
      </Layout>
    )
  }

  if (!cart || cart.items.length === 0) {
    return (
      <Layout>
        <div className="max-w-2xl mx-auto text-center py-12">
          <div className="text-6xl mb-4">🛒</div>
          <h2 className="text-2xl font-bold mb-4">Your cart is empty</h2>
          <p className="text-gray-600 mb-8">
            Start adding spiritual products to your cart!
          </p>
          <Link
            href="/products"
            className="inline-block bg-orange-500 text-white px-8 py-3 rounded-lg hover:bg-orange-600"
          >
            Browse Products
          </Link>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          {cart.items.map((item: any) => (
            <div
              key={item.id}
              className="flex items-center gap-4 py-4 border-b last:border-b-0"
            >
              <div className="w-20 h-20 bg-gradient-to-br from-orange-100 to-red-100 rounded flex items-center justify-center flex-shrink-0">
                <span className="text-3xl">🙏</span>
              </div>

              <div className="flex-grow">
                <h3 className="font-bold">{item.product.name}</h3>
                <p className="text-sm text-gray-600">{item.product.category_name}</p>
                <p className="text-orange-600 font-semibold mt-1">
                  ₹{item.product.effective_price}
                </p>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  className="w-8 h-8 flex items-center justify-center border rounded hover:bg-gray-100"
                >
                  -
                </button>
                <span className="w-8 text-center font-semibold">{item.quantity}</span>
                <button
                  onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  className="w-8 h-8 flex items-center justify-center border rounded hover:bg-gray-100"
                >
                  +
                </button>
              </div>

              <div className="text-right">
                <p className="font-bold">₹{item.subtotal}</p>
                <button
                  onClick={() => removeItem(item.id)}
                  className="text-sm text-red-600 hover:text-red-800 mt-1"
                >
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="space-y-2 mb-6">
            <div className="flex justify-between text-gray-600">
              <span>Subtotal ({cart.total_items} items)</span>
              <span>₹{cart.total_price}</span>
            </div>
            <div className="flex justify-between text-gray-600">
              <span>Shipping</span>
              <span className="text-green-600">Free</span>
            </div>
            <div className="border-t pt-2 flex justify-between font-bold text-lg">
              <span>Total</span>
              <span className="text-orange-600">₹{cart.total_price}</span>
            </div>
          </div>

          <div className="flex gap-4">
            <Link
              href="/products"
              className="flex-1 text-center border border-gray-300 px-6 py-3 rounded-lg hover:bg-gray-50"
            >
              Continue Shopping
            </Link>
            <button
              onClick={handleCheckout}
              disabled={checkoutLoading}
              className="flex-1 bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 font-semibold disabled:bg-gray-400"
            >
              {checkoutLoading ? 'Processing...' : 'Proceed to Checkout'}
            </button>
          </div>

          <p className="text-sm text-gray-600 text-center mt-4">
            Secure checkout • Free shipping on all orders
          </p>
        </div>
      </div>
    </Layout>
  )
}
