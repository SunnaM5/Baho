'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ApiService } from '@/lib/api'

interface BrandItem {
  id: string
  name: string
  logo?: string
}

// Crisp inline vector logos
const AppleIcon = () => (
  <svg className="h-7 sm:h-8 w-auto fill-slate-700" viewBox="0 0 24 24">
    <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.32c.67-.82 1.13-1.96.99-3.11-1 .04-2.21.67-2.92 1.5-.64.74-1.2 1.92-1.04 3.06 1.12.09 2.26-.54 2.97-1.45z" />
  </svg>
)

const SamsungIcon = () => (
  <span className="text-xl sm:text-2xl font-black tracking-widest text-slate-700 font-sans uppercase">
    SAMSUNG
  </span>
)

const XiaomiIcon = () => (
  <span className="text-xl sm:text-2xl font-black tracking-wider text-slate-700 font-sans uppercase">
    XIAOMI
  </span>
)

const HuaweiIcon = () => (
  <span className="text-xl sm:text-2xl font-black tracking-wider text-slate-700 font-sans uppercase">
    HUAWEI
  </span>
)

const HonorIcon = () => (
  <span className="text-xl sm:text-2xl font-black tracking-widest text-slate-700 font-sans uppercase">
    HONOR
  </span>
)

export function Brands() {
  const [brands, setBrands] = useState<BrandItem[]>([])

  useEffect(() => {
    ApiService.getBrands()
      .then((data) => {
        const list = Array.isArray(data) ? data : data.results || []
        setBrands(list)
      })
      .catch((err) => console.error('Failed to load brands:', err))
  }, [])

  const defaultList = [
    { id: '1', name: 'Apple', icon: <AppleIcon /> },
    { id: '2', name: 'Samsung', icon: <SamsungIcon /> },
    { id: '3', name: 'Xiaomi', icon: <XiaomiIcon /> },
    { id: '4', name: 'Huawei', icon: <HuaweiIcon /> },
    { id: '5', name: 'Honor', icon: <HonorIcon /> },
  ]

  const getBrandIcon = (name: string) => {
    const lower = name.toLowerCase()
    if (lower.includes('apple')) return <AppleIcon />
    if (lower.includes('samsung')) return <SamsungIcon />
    if (lower.includes('xiaomi')) return <XiaomiIcon />
    if (lower.includes('huawei')) return <HuaweiIcon />
    if (lower.includes('honor')) return <HonorIcon />
    return (
      <span className="text-xl sm:text-2xl font-black tracking-wider text-slate-700 font-sans uppercase">
        {name}
      </span>
    )
  }

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

  const itemsToRender = brands.length > 0
    ? brands.map((b, i) => {
        let logoUrl = b.logo
        if (logoUrl && typeof logoUrl === 'string' && !logoUrl.startsWith('http')) {
          logoUrl = `${API_BASE_URL}${logoUrl}`
        }
        return {
          id: b.id || String(i),
          name: b.name,
          logoUrl: logoUrl || null,
          icon: getBrandIcon(b.name),
        }
      })
    : defaultList

  const tickerItems = [...itemsToRender, ...itemsToRender, ...itemsToRender, ...itemsToRender]

  return (
    <section className="py-8 my-6 bg-white border-y border-slate-200/80 overflow-hidden relative select-none">
      <div className="absolute left-0 top-0 bottom-0 w-24 z-10 bg-gradient-to-r from-white to-transparent pointer-events-none" />
      <div className="absolute right-0 top-0 bottom-0 w-24 z-10 bg-gradient-to-l from-white to-transparent pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 mb-4 text-center">
        <span className="text-[11px] font-black text-slate-400 uppercase tracking-widest">
          Официальные бренды
        </span>
      </div>

      <div className="flex overflow-hidden">
        <motion.div
          animate={{ x: ['0%', '-50%'] }}
          transition={{
            ease: 'linear',
            duration: 25,
            repeat: Infinity,
          }}
          className="flex items-center gap-12 sm:gap-20 whitespace-nowrap min-w-full"
        >
          {tickerItems.map((brand, idx) => (
            <div
              key={`${brand.id}-${idx}`}
              className="flex items-center justify-center opacity-85 hover:opacity-100 transition-all duration-300 cursor-pointer py-2 px-4"
            >
              {brand.logoUrl ? (
                <img
                  src={brand.logoUrl}
                  alt={brand.name}
                  className="h-8 sm:h-11 max-w-[150px] w-auto object-contain mix-blend-multiply contrast-125"
                />
              ) : (
                brand.icon
              )}
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
