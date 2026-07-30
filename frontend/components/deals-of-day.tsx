'use client'

import { motion } from 'framer-motion'
import { Clock, Flame, ArrowRight } from 'lucide-react'
import { ProductCard } from './product-card'
import { useState, useEffect } from 'react'
import { ApiService } from '@/lib/api'
import { useLanguage } from '@/context/language-context'

export function DealsOfDay() {
  const { t } = useLanguage()
  const [dealProducts, setDealProducts] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [timeLeft, setTimeLeft] = useState({
    hours: 0,
    minutes: 0,
    seconds: 0,
  })

  useEffect(() => {
    ApiService.getProducts()
      .then((res) => {
        const list = Array.isArray(res) ? res : res.results || []
        setDealProducts(list.slice(0, 4))
      })
      .catch((err) => console.error('Failed to load deals:', err))
      .finally(() => setLoading(false))

    const timer = setInterval(() => {
      const now = new Date()
      const tomorrow = new Date(now)
      tomorrow.setDate(tomorrow.getDate() + 1)
      tomorrow.setHours(0, 0, 0, 0)

      const diff = tomorrow.getTime() - now.getTime()
      const hours = Math.floor((diff / (1000 * 60 * 60)) % 24)
      const minutes = Math.floor((diff / (1000 * 60)) % 60)
      const seconds = Math.floor((diff / 1000) % 60)

      setTimeLeft({ hours, minutes, seconds })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  if (loading) {
    return <div className="py-16 text-center text-slate-500 font-bold">{t('loadingDeals')}</div>
  }

  return (
    <section className="py-8 lg:py-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mb-8"
      >
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Flame className="w-5 h-5 text-emerald-600" />
              <h2 className="text-2xl lg:text-3xl font-black text-slate-900">{t('dealsOfDayTitle')}</h2>
            </div>
            <p className="text-slate-500 font-medium text-xs sm:text-sm">
              {t('dealsOfDaySubtitle')}
            </p>
          </div>

          <motion.div
            animate={{ scale: [1, 1.02, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="flex gap-2.5 bg-emerald-50 border border-emerald-200 rounded-xl px-4 py-2.5 w-fit"
          >
            <Clock className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <div className="flex gap-3 font-bold text-emerald-800 text-xs">
              <div>
                {String(timeLeft.hours).padStart(2, '0')}h
              </div>
              <div>
                {String(timeLeft.minutes).padStart(2, '0')}m
              </div>
              <div>
                {String(timeLeft.seconds).padStart(2, '0')}s
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6"
      >
        {dealProducts.map((product, index) => (
          <motion.div
            key={product.id}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.1 }}
          >
            <ProductCard product={product} />
          </motion.div>
        ))}
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mt-12 text-center"
      >
        <a
          href="/catalog"
          className="inline-flex items-center gap-2 px-8 py-4 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl transition shadow-lg shadow-emerald-700/20 mx-auto"
        >
          {t('viewAllDeals')}
          <ArrowRight className="w-5 h-5" />
        </a>
      </motion.div>
    </section>
  )
}
