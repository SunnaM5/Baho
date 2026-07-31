'use client'

import { motion } from 'framer-motion'
import { Heart, ShoppingCart, Star, ShieldCheck, Zap, Check, BatteryCharging } from 'lucide-react'
import { useState } from 'react'
import Link from 'next/link'
import { ApiService } from '@/lib/api'

import { useLanguage } from '@/context/language-context'

interface ProductCardProps {
  product: {
    id: string
    name: string
    name_uz?: string
    name_en?: string
    brand?: { name: string } | string
    base_price?: number | string
    price?: number
    discount?: number
    battery_health?: number
    images?: { image: string }[]
    image?: string
    rating?: number
    reviews_count?: number
    reviews?: number
    stock?: number
    inStock?: boolean
  }
}

export function ProductCard({ product }: ProductCardProps) {
  const { lang, t } = useLanguage()
  const [isWishlisted, setIsWishlisted] = useState(false)
  const [isAdded, setIsAdded] = useState(false)
  const [isHovered, setIsHovered] = useState(false)

  const productName = (lang === 'uz' && product.name_uz)
    ? product.name_uz
    : (lang === 'en' && product.name_en)
    ? product.name_en
    : product.name

  const rawPrice = Number(product.base_price || product.price || 0)
  const brandName = typeof product.brand === 'object' ? product.brand?.name : product.brand || 'BAHO'
  const imageUrl = (product as any).main_image || product.images?.[0]?.image || product.image || 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=500'
  const inStock = product.stock !== undefined ? product.stock > 0 : product.inStock ?? true

  const formattedPrice = new Intl.NumberFormat('ru-RU').format(rawPrice)
  const numericDiscountedPrice = product.discount
    ? Math.round(rawPrice * (1 - product.discount / 100))
    : rawPrice
  const discountedPrice = new Intl.NumberFormat('ru-RU').format(numericDiscountedPrice)
  const monthlyPayment = new Intl.NumberFormat('ru-RU').format(Math.round(numericDiscountedPrice / 12))

  // Instant Optimistic Toggle for Wishlist
  const handleToggleWishlist = async () => {
    setIsWishlisted((prev) => !prev) // Instant state change
    try {
      await ApiService.toggleFavorite(product.id)
    } catch (e) {
      console.error('Wishlist sync error:', e)
    }
  }

  // Instant Optimistic Feedback for Cart
  const handleAddToCart = async () => {
    setIsAdded(true) // Instant feedback
    setTimeout(() => setIsAdded(false), 1800)

    try {
      await ApiService.addToCart(product.id, 1)
    } catch (e) {
      console.error('Cart sync error:', e)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -8 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="group relative bg-white rounded-2xl border border-emerald-100/80 hover:border-emerald-500/40 shadow-sm hover:shadow-2xl hover:shadow-emerald-900/10 transition-all duration-300 flex flex-col overflow-hidden"
    >
      {/* Dynamic Top Glow on Hover */}
      <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-emerald-600 via-green-500 to-emerald-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10" />

      {/* Image Container */}
      <Link href={`/product/${product.id}`} className="relative h-40 sm:h-56 md:h-64 overflow-hidden bg-gradient-to-b from-slate-50 to-emerald-50/30 flex items-center justify-center p-2 sm:p-4">
        <motion.img
          src={imageUrl}
          alt={productName}
          className="w-full h-full object-contain drop-shadow-md"
          animate={{ scale: isHovered ? 1.08 : 1 }}
          transition={{ duration: 0.3 }}
        />

        {/* Badges */}
        <div className="absolute top-2 left-2 sm:top-3 sm:left-3 flex flex-col gap-1 z-10">
          <span className="inline-flex items-center gap-1 bg-emerald-900/90 backdrop-blur-md text-emerald-100 text-[10px] sm:text-[11px] font-bold px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-full shadow-sm">
            <Zap className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-emerald-400 fill-emerald-400" /> 0-0-12
          </span>
          {product.battery_health && (
            <span className="inline-flex items-center gap-1 bg-amber-600 text-white text-[10px] sm:text-[11px] font-bold px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-full shadow-sm">
              <BatteryCharging className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-amber-200" /> АКБ {product.battery_health}%
            </span>
          )}
          {product.discount && (
            <span className="inline-flex items-center gap-1 bg-rose-500 text-white text-[10px] sm:text-[11px] font-bold px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-full shadow-sm">
              -{product.discount}%
            </span>
          )}
        </div>

        {/* Wishlist Button (Instant click response) */}
        <motion.button
          whileHover={{ scale: 1.15 }}
          whileTap={{ scale: 0.85 }}
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
            handleToggleWishlist()
          }}
          className={`absolute top-2 right-2 sm:top-3 sm:right-3 z-10 p-2 sm:p-2.5 rounded-full backdrop-blur-md transition-all shadow-sm ${
            isWishlisted
              ? 'bg-rose-50 text-rose-500 shadow-rose-200'
              : 'bg-white/80 hover:bg-white text-slate-400 hover:text-rose-500'
          }`}
        >
          <Heart className="w-3.5 h-3.5 sm:w-4 sm:h-4" fill={isWishlisted ? 'currentColor' : 'none'} />
        </motion.button>

        {!inStock && (
          <div className="absolute inset-0 bg-slate-900/60 backdrop-blur-[2px] flex items-center justify-center z-10">
            <span className="bg-white/90 text-slate-800 text-[10px] sm:text-xs font-bold px-3 py-1.5 rounded-full uppercase tracking-wider shadow-lg">
              {lang === 'uz' ? 'Mavjud emas' : lang === 'en' ? 'Out of stock' : 'Нет в наличии'}
            </span>
          </div>
        )}
      </Link>

      {/* Content */}
      <div className="p-3 sm:p-5 flex flex-col flex-1 bg-white">
        <div className="flex items-center justify-between text-[10px] sm:text-xs text-emerald-700 font-bold uppercase tracking-wider mb-1">
          <span>{brandName}</span>
          <span className="hidden sm:flex text-slate-400 text-[11px] items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> {t('warrantyOneYear')}
          </span>
        </div>

        <Link href={`/product/${product.id}`}>
          <h3 className="font-semibold text-slate-900 text-xs sm:text-base leading-tight sm:leading-snug mb-1.5 sm:mb-2 line-clamp-2 group-hover:text-emerald-700 transition-colors cursor-pointer">
            {productName}
          </h3>
        </Link>

        {/* Rating */}
        <div className="flex items-center gap-2 mb-3">
          <div className="flex gap-0.5">
            {[...Array(5)].map((_, i) => (
              <Star
                key={i}
                className={`w-3.5 h-3.5 ${
                  i < Math.floor(product.rating || 5)
                    ? 'fill-amber-400 text-amber-400'
                    : 'text-slate-200'
                }`}
              />
            ))}
          </div>
          <span className="text-xs text-slate-400 font-medium">
            ({product.reviews_count || product.reviews || 12})
          </span>
        </div>

        {/* Installment Highlight Box */}
        <div className="bg-emerald-50/70 border border-emerald-200/60 rounded-xl p-2.5 mb-3 flex items-center justify-between">
          <span className="text-[11px] font-semibold text-emerald-800">{t('installmentLabel')}</span>
          <span className="text-xs font-bold text-emerald-900">
            {t('fromPrefix')} {monthlyPayment} {t('sum')}/{t('monthShort')}
          </span>
        </div>

        {/* Price & Instant Cart CTA */}
        <div className="mt-auto pt-2 flex items-center justify-between gap-3">
          <div>
            {product.discount && (
              <span className="block text-xs text-slate-400 line-through font-medium">
                {formattedPrice} {t('sum')}
              </span>
            )}
            <span className="text-lg font-extrabold text-slate-900 leading-none">
              {discountedPrice} <span className="text-xs font-semibold text-slate-500">{t('sum')}</span>
            </span>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleAddToCart}
            disabled={!inStock}
            className={`p-3 text-white rounded-xl shadow-md transition-all flex items-center justify-center disabled:opacity-50 ${
              isAdded
                ? 'bg-emerald-600 shadow-emerald-500/30 ring-2 ring-emerald-400'
                : 'bg-emerald-800 hover:bg-emerald-900 shadow-emerald-900/20'
            }`}
          >
            {isAdded ? <Check className="w-5 h-5" /> : <ShoppingCart className="w-5 h-5" />}
          </motion.button>
        </div>
      </div>
    </motion.div>
  )
}
