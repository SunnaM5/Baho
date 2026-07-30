'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Star, ChevronLeft, ChevronRight } from 'lucide-react'
import { fetchAPI } from '@/lib/api'

interface ReviewItem {
  id: string
  user_name?: string
  name?: string
  rating: number
  comment?: string
  text?: string
  avatar?: string
}

export function Reviews() {
  const [reviews, setReviews] = useState<ReviewItem[]>([])
  const [current, setCurrent] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI('/api/v1/cms/home/')
      .then((res) => {
        const list = res?.faqs || res?.reviews || [
          {
            id: '1',
            name: 'Akmal Hoshimov',
            rating: 5,
            text: 'Amazing service and fast delivery in Tashkent!',
            avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
          }
        ]
        setReviews(list)
      })
      .catch((err) => console.error('Failed to load reviews:', err))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="py-16 text-center text-muted-foreground">Loading reviews...</div>
  }

  if (!reviews.length) {
    return null
  }

  const currentItem = reviews[current] || reviews[0]

  const next = () => {
    setCurrent((prev) => (prev + 1) % reviews.length)
  }

  const prev = () => {
    setCurrent((prev) => (prev - 1 + reviews.length) % reviews.length)
  }

  return (
    <section className="py-16 lg:py-24">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mb-12 text-center"
      >
        <h2 className="text-3xl lg:text-4xl font-bold mb-4">
          Customer Reviews
        </h2>
        <p className="text-muted-foreground">
          Join thousands of happy customers who trust BAHO Market
        </p>
      </motion.div>

      <div className="grid lg:grid-cols-3 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-8 border border-primary/20"
        >
          <div className="flex items-start justify-between mb-4">
            <div className="flex gap-1">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-5 h-5 fill-accent text-accent" />
              ))}
            </div>
            <span className="text-3xl font-bold text-primary">4.9</span>
          </div>
          <p className="text-muted-foreground mb-2">Based on verified orders</p>
          <div className="w-full bg-secondary rounded-full h-2">
            <motion.div
              initial={{ width: 0 }}
              whileInView={{ width: '98%' }}
              transition={{ delay: 0.3, duration: 1 }}
              className="h-full bg-primary rounded-full"
            />
          </div>
        </motion.div>

        {[
          { label: 'Happy Customers', value: '15K+' },
          { label: 'Products Sold', value: '50K+' },
          { label: 'Years in Business', value: '5+' },
        ].map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.1 }}
            className="bg-card border border-border rounded-2xl p-8 text-center"
          >
            <div className="text-3xl font-bold text-primary mb-2">
              {stat.value}
            </div>
            <p className="text-muted-foreground">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="relative"
      >
        <div className="overflow-hidden">
          <motion.div
            key={`testimonial-${current}`}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            className="bg-card border border-border rounded-2xl p-8 md:p-12"
          >
            <div className="flex gap-1 mb-4">
              {[...Array(currentItem.rating || 5)].map((_, i) => (
                <Star key={i} className="w-5 h-5 fill-accent text-accent" />
              ))}
            </div>

            <p className="text-xl md:text-2xl mb-6 italic text-foreground">
              &ldquo;{currentItem.text || currentItem.comment || 'Verified purchase'}&rdquo;
            </p>

            <div className="flex items-center gap-4">
              <img
                src={currentItem.avatar || 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100'}
                alt={currentItem.name || currentItem.user_name || 'User'}
                className="w-14 h-14 rounded-full object-cover"
              />
              <div>
                <h4 className="font-bold text-lg">{currentItem.name || currentItem.user_name || 'Verified Customer'}</h4>
                <p className="text-sm text-muted-foreground">Verified Customer</p>
              </div>
            </div>
          </motion.div>
        </div>

        <div className="flex justify-center gap-4 mt-8">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={prev}
            className="p-2 rounded-full border border-border hover:border-primary hover:bg-primary/10 transition"
          >
            <ChevronLeft className="w-6 h-6" />
          </motion.button>

          <div className="flex gap-2 items-center">
            {reviews.map((_, index) => (
              <motion.button
                key={index}
                onClick={() => setCurrent(index)}
                className={`h-2 rounded-full transition ${
                  current === index ? 'bg-primary w-8' : 'bg-border w-2'
                }`}
                whileHover={{ scale: 1.2 }}
              />
            ))}
          </div>

          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={next}
            className="p-2 rounded-full border border-border hover:border-primary hover:bg-primary/10 transition"
          >
            <ChevronRight className="w-6 h-6" />
          </motion.button>
        </div>
      </motion.div>
    </section>
  )
}
