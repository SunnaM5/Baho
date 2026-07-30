'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Trash2, Plus, Minus, ArrowRight, ShoppingCart, ShieldCheck } from 'lucide-react'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { ApiService } from '@/lib/api'
import Link from 'next/link'

export default function CartPage() {
  const [cart, setCart] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  const loadCart = async () => {
    try {
      const data = await ApiService.getCart().catch(() => ({ items: [], total_price: 0 }))
      setCart(data)
    } catch (e) {
      console.error('Cart fetch failed:', e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCart()
  }, [])

  const cartItems = cart?.items || []
  const totalAmount = Number(cart?.total_price || cart?.total || 0)
  const monthlyPayment = new Intl.NumberFormat('en-US').format(Math.round(totalAmount / 12))

  const handleQuantityChange = async (itemId: string, delta: number) => {
    const item = cartItems.find((i: any) => i.id === itemId)
    if (!item) return
    const newQty = item.quantity + delta
    if (newQty <= 0) return

    // Optimistic UI update
    setCart((prev: any) => ({
      ...prev,
      items: prev.items.map((i: any) =>
        i.id === itemId ? { ...i, quantity: newQty } : i
      ),
      total_price: prev.total_price + delta * (i.product?.price || i.product?.base_price || 0),
    }))

    try {
      await ApiService.addToCart(item.product.id || item.product_id, delta)
      await loadCart()
    } catch (e) {
      console.error('Failed updating quantity:', e)
    }
  }

  if (loading) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-slate-50 py-20 text-center font-medium text-slate-500">
          Загрузка корзины...
        </main>
        <Footer />
      </>
    )
  }

  return (
    <>
      <Header />
      <main className="min-h-screen bg-slate-50">
        <div className="border-b border-slate-200 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-500">
              <Link href="/" className="hover:text-emerald-800 transition">Главная</Link>
              <span>/</span>
              <span className="text-slate-900 font-bold">Корзина покупок</span>
            </div>
          </div>
        </div>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
          {cartItems.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-3xl p-12 text-center border border-slate-200/80 shadow-sm max-w-xl mx-auto my-8"
            >
              <div className="w-20 h-20 mx-auto mb-5 bg-emerald-50 rounded-full flex items-center justify-center text-emerald-800">
                <ShoppingCart className="w-10 h-10" />
              </div>
              <h2 className="text-2xl font-black text-slate-900 mb-3">Ваша корзина пуста</h2>
              <p className="text-slate-500 text-sm mb-8 leading-relaxed">
                Выберите подходящие товары из каталога и добавьте их в корзину.
              </p>
              <Link
                href="/"
                className="inline-flex items-center gap-2 px-8 py-3.5 bg-emerald-800 hover:bg-emerald-900 text-white font-bold text-sm rounded-xl transition-all shadow-md hover:shadow-lg"
              >
                <ArrowRight className="w-4 h-4" /> Перейти к покупкам
              </Link>
            </motion.div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* Items List */}
              <div className="lg:col-span-8 space-y-4">
                <h1 className="text-2xl sm:text-3xl font-black text-slate-900 mb-4">
                  Корзина товаров ({cartItems.length})
                </h1>

                <div className="space-y-3">
                  {cartItems.map((item: any) => {
                    const product = item.product || {}
                    const price = Number(product.base_price || product.price || 0)
                    const itemTotal = price * item.quantity

                    return (
                      <motion.div
                        key={item.id}
                        layout
                        className="p-4 sm:p-5 bg-white rounded-2xl border border-slate-200/80 shadow-sm flex flex-col sm:flex-row items-center gap-4 sm:gap-6"
                      >
                        <div className="w-24 h-24 sm:w-28 sm:h-28 flex-shrink-0 bg-slate-50 rounded-xl overflow-hidden p-2 flex items-center justify-center">
                          <img
                            src={product.images?.[0]?.image || 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=500'}
                            alt={product.name || 'Товар'}
                            className="w-full h-full object-contain"
                          />
                        </div>

                        <div className="flex-1 w-full text-center sm:text-left">
                          <span className="text-[11px] font-extrabold text-emerald-800 uppercase tracking-wider block mb-1">
                            {product.brand?.name || product.brand || 'BAHO'}
                          </span>
                          <h3 className="font-bold text-slate-900 text-base leading-snug mb-2 line-clamp-2">
                            {product.name}
                          </h3>
                          <span className="text-sm font-extrabold text-slate-900">
                            {new Intl.NumberFormat('en-US').format(Math.round(price))} сум
                          </span>
                        </div>

                        {/* Quantity & Item Subtotal */}
                        <div className="flex items-center justify-between sm:justify-end gap-6 w-full sm:w-auto pt-3 sm:pt-0 border-t sm:border-t-0 border-slate-100">
                          <div className="flex items-center gap-2 bg-slate-100 rounded-xl p-1">
                            <button
                              onClick={() => handleQuantityChange(item.id, -1)}
                              className="w-8 h-8 rounded-lg bg-white hover:bg-slate-200 text-slate-900 font-bold transition flex items-center justify-center shadow-xs text-sm"
                            >
                              <Minus className="w-3.5 h-3.5" />
                            </button>
                            <span className="w-6 text-center font-bold text-sm">{item.quantity}</span>
                            <button
                              onClick={() => handleQuantityChange(item.id, 1)}
                              className="w-8 h-8 rounded-lg bg-white hover:bg-slate-200 text-slate-900 font-bold transition flex items-center justify-center shadow-xs text-sm"
                            >
                              <Plus className="w-3.5 h-3.5" />
                            </button>
                          </div>

                          <span className="text-base font-black text-emerald-900 min-w-[100px] text-right">
                            {new Intl.NumberFormat('en-US').format(Math.round(itemTotal))} сум
                          </span>
                        </div>
                      </motion.div>
                    )
                  })}
                </div>
              </div>

              {/* Order Summary Column */}
              <div className="lg:col-span-4">
                <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm space-y-6 sticky top-24">
                  <h2 className="text-xl font-black text-slate-900">Итого заказа</h2>

                  <div className="space-y-4 text-sm border-t border-slate-100 pt-4">
                    <div className="flex justify-between text-slate-600">
                      <span>Стоимость товаров:</span>
                      <span className="font-bold text-slate-900">{new Intl.NumberFormat('en-US').format(Math.round(totalAmount))} сум</span>
                    </div>

                    <div className="flex justify-between text-slate-600">
                      <span>Доставка по Ташкенту:</span>
                      <span className="font-bold text-emerald-700">Бесплатно</span>
                    </div>

                    <div className="bg-emerald-50 border border-emerald-200/80 rounded-xl p-3.5 text-xs text-emerald-900">
                      <span className="font-bold block mb-0.5">В рассрочку без переплат:</span>
                      <strong className="text-sm font-black text-emerald-800">от {monthlyPayment} сум/мес</strong>
                    </div>

                    <div className="border-t border-slate-200 pt-4 flex justify-between items-baseline">
                      <span className="text-base font-bold text-slate-900">Всего к оплате:</span>
                      <span className="text-2xl font-black text-slate-900">
                        {new Intl.NumberFormat('en-US').format(Math.round(totalAmount))} сум
                      </span>
                    </div>

                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      className="w-full py-4 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl font-bold text-base shadow-md hover:shadow-lg shadow-emerald-900/20 transition-all mt-4"
                    >
                      Оформить заказ
                    </motion.button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>
      </main>
      <Footer />
    </>
  )
}
