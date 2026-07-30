'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Trash2, Heart, ArrowLeft } from 'lucide-react'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { ApiService } from '@/lib/api'
import { ProductCard } from '@/components/product-card'
import Link from 'next/link'

export default function WishlistPage() {
  const [wishlist, setWishlist] = useState<any[]>([])
  const [recommendations, setRecommendations] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  const loadWishlist = async () => {
    try {
      const res = await ApiService.getFavorites().catch(() => [])
      const list = Array.isArray(res) ? res : res.results || []
      setWishlist(list)

      const recRes = await ApiService.getProducts().catch(() => [])
      const recList = Array.isArray(recRes) ? recRes : recRes.results || []
      setRecommendations(recList.slice(0, 4))
    } catch (e) {
      console.error('Wishlist fetch error:', e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadWishlist()
  }, [])

  const handleRemoveItem = async (productId: string) => {
    try {
      await ApiService.toggleFavorite(productId).catch(() => {})
      setWishlist((prev) => prev.filter((item) => (item.product?.id || item.id) !== productId))
    } catch (e) {
      console.error('Failed to remove item:', e)
    }
  }

  if (loading) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-slate-50 py-20 text-center font-medium text-slate-500">
          Загрузка избранного...
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
              <span className="text-slate-900 font-bold">Моё Избранное</span>
            </div>
          </div>
        </div>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          {wishlist.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-3xl p-12 text-center border border-slate-200/80 shadow-sm max-w-xl mx-auto my-8"
            >
              <div className="w-20 h-20 mx-auto mb-5 bg-rose-50 rounded-full flex items-center justify-center text-rose-500">
                <Heart className="w-10 h-10" />
              </div>
              <h2 className="text-2xl font-black text-slate-900 mb-3">Ваш список избранного пуст</h2>
              <p className="text-slate-500 text-sm mb-8 leading-relaxed">
                Добавляйте понравившиеся смартфоны и гаджеты, нажав на сердечко на карточке товара.
              </p>
              <Link
                href="/"
                className="inline-flex items-center gap-2 px-8 py-3.5 bg-emerald-800 hover:bg-emerald-900 text-white font-bold text-sm rounded-xl transition-all shadow-md hover:shadow-lg"
              >
                <ArrowLeft className="w-4 h-4" /> Перейти к покупкам
              </Link>
            </motion.div>
          ) : (
            <div>
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
                <div>
                  <h1 className="text-3xl font-black text-slate-900 tracking-tight">Избранные товары</h1>
                  <p className="text-slate-500 text-sm mt-1">
                    Сохранено товаров: <strong className="text-emerald-800 font-bold">{wishlist.length}</strong>
                  </p>
                </div>
              </div>

              <motion.div
                layout
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
              >
                {wishlist.map((item, index) => {
                  const product = item.product || item
                  const rawPrice = Number(product.base_price || product.price || 0)

                  return (
                    <motion.div
                      key={item.id || index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      layout
                      className="group bg-white rounded-2xl overflow-hidden border border-slate-200 hover:border-emerald-500/50 shadow-sm hover:shadow-xl transition-all flex flex-col relative"
                    >
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => handleRemoveItem(product.id)}
                        className="absolute top-3 right-3 z-10 p-2.5 bg-white/90 hover:bg-rose-500 hover:text-white text-slate-400 rounded-full shadow-md transition-all"
                        title="Удалить"
                      >
                        <Trash2 className="w-4 h-4" />
                      </motion.button>

                      <div className="relative h-60 overflow-hidden bg-slate-50 flex items-center justify-center p-4">
                        <img
                          src={product.images?.[0]?.image || 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=500'}
                          alt={product.name || 'Товар'}
                          className="w-full h-full object-contain"
                        />
                      </div>

                      <div className="p-5 flex flex-col flex-1">
                        <p className="text-xs text-emerald-800 font-bold uppercase tracking-wider mb-1">
                          {product.brand?.name || product.brand || 'BAHO'}
                        </p>

                        <h3 className="font-semibold text-slate-900 mb-3 line-clamp-2 text-sm leading-snug">
                          {product.name}
                        </h3>

                        <div className="mt-auto pt-2">
                          <span className="text-lg font-black text-slate-900">
                            {new Intl.NumberFormat('en-US').format(Math.round(rawPrice))} сум
                          </span>
                        </div>
                      </div>
                    </motion.div>
                  )
                })}
              </motion.div>

              {recommendations.length > 0 && (
                <div className="mt-16 pt-10 border-t border-slate-200">
                  <h3 className="text-2xl font-black text-slate-900 mb-6">Вам также может понравиться</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    {recommendations.map((product) => (
                      <ProductCard key={product.id} product={product} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </section>
      </main>
      <Footer />
    </>
  )
}
