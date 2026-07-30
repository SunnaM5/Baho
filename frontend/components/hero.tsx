'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sparkles, ArrowRight } from 'lucide-react'
import { useLanguage } from '@/context/language-context'

interface HeroSlide {
  id: string
  topBadgeRu: string
  topBadgeUz: string
  topBadgeEn: string
  titleLine1Ru: string
  titleLine1Uz: string
  titleLine1En: string
  titleLine2Ru: string
  titleLine2Uz: string
  titleLine2En: string
  pillBadgeRu: string
  pillBadgeUz: string
  pillBadgeEn: string
  detailsRu: string
  detailsUz: string
  detailsEn: string
  image: string
}

const heroSlides: HeroSlide[] = [
  {
    id: '1',
    topBadgeRu: 'РАССРОЧКА ДО 12 МЕСЯЦЕВ',
    topBadgeUz: '12 OYGACHA BOʻLIB TOʻLASH',
    topBadgeEn: 'UP TO 12 MONTHS INSTALLMENT',
    titleLine1Ru: 'iPhone',
    titleLine1Uz: 'iPhone',
    titleLine1En: 'iPhone',
    titleLine2Ru: 'в рассрочку',
    titleLine2Uz: 'boʻlib toʻlashga',
    titleLine2En: 'in installments',
    pillBadgeRu: 'Без первоначального взноса',
    pillBadgeUz: 'Boshlangʻich toʻlovsiz',
    pillBadgeEn: 'Zero down payment',
    detailsRu: 'от 499 000 сум/мес  •  официальная гарантия 12 мес',
    detailsUz: '499 000 soʻm/oydan  •  rasmiy kafolat 12 oy',
    detailsEn: 'from 499,000 sum/mo  •  12 months official warranty',
    image: '/hero_iphone_exact_banner.png',
  },
  {
    id: '2',
    topBadgeRu: 'РАССРОЧКА ДО 12 МЕСЯЦЕВ',
    topBadgeUz: '12 OYGACHA BOʻLIB TOʻLASH',
    topBadgeEn: 'UP TO 12 MONTHS INSTALLMENT',
    titleLine1Ru: 'Samsung Galaxy',
    titleLine1Uz: 'Samsung Galaxy',
    titleLine1En: 'Samsung Galaxy',
    titleLine2Ru: 'в рассрочку',
    titleLine2Uz: 'boʻlib toʻlashga',
    titleLine2En: 'in installments',
    pillBadgeRu: 'Galaxy AI внутри',
    pillBadgeUz: 'Galaxy AI mavjud',
    pillBadgeEn: 'Galaxy AI included',
    detailsRu: 'от 450 000 сум/мес  •  официальная гарантия 12 мес',
    detailsUz: '450 000 soʻm/oydan  •  rasmiy kafolat 12 oy',
    detailsEn: 'from 450,000 sum/mo  •  12 months official warranty',
    image: '/samsung_s24_hero.png',
  },
  {
    id: '3',
    topBadgeRu: 'РАССРОЧКА ДО 12 МЕСЯЦЕВ',
    topBadgeUz: '12 OYGACHA BOʻLIB TOʻLASH',
    topBadgeEn: 'UP TO 12 MONTHS INSTALLMENT',
    titleLine1Ru: 'MacBook Pro M3',
    titleLine1Uz: 'MacBook Pro M3',
    titleLine1En: 'MacBook Pro M3',
    titleLine2Ru: 'для профессионалов',
    titleLine2Uz: 'professional darajada',
    titleLine2En: 'for professionals',
    pillBadgeRu: 'Беспроцентный тариф',
    pillBadgeUz: 'Ustamasiz tarif',
    pillBadgeEn: 'Zero interest plan',
    detailsRu: 'от 1 200 000 сум/мес  •  гарантия от производителя',
    detailsUz: '1 200 000 soʻm/oydan  •  ishlab chiqaruvchi kafolati',
    detailsEn: 'from 1,200,000 sum/mo  •  official warranty',
    image: '/macbook_pro_hero.png',
  },
]

export function Hero() {
  const [current, setCurrent] = useState(0)
  const { lang } = useLanguage()

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % heroSlides.length)
    }, 6000)
    return () => clearInterval(timer)
  }, [])

  const handleDragEnd = (event: any, info: any) => {
    const swipeThreshold = 40
    if (info.offset.x < -swipeThreshold) {
      setCurrent((prev) => (prev + 1) % heroSlides.length)
    } else if (info.offset.x > swipeThreshold) {
      setCurrent((prev) => (prev - 1 + heroSlides.length) % heroSlides.length)
    }
  }

  const activeSlide = heroSlides[current]
  const langKey = lang as 'ru' | 'uz' | 'en'

  const topBadge = activeSlide[`topBadge${langKey.charAt(0).toUpperCase() + langKey.slice(1)}` as keyof HeroSlide] as string
  const title1 = activeSlide[`titleLine1${langKey.charAt(0).toUpperCase() + langKey.slice(1)}` as keyof HeroSlide] as string
  const title2 = activeSlide[`titleLine2${langKey.charAt(0).toUpperCase() + langKey.slice(1)}` as keyof HeroSlide] as string
  const pillBadge = activeSlide[`pillBadge${langKey.charAt(0).toUpperCase() + langKey.slice(1)}` as keyof HeroSlide] as string
  const details = activeSlide[`details${langKey.charAt(0).toUpperCase() + langKey.slice(1)}` as keyof HeroSlide] as string

  return (
    <section className="relative rounded-2xl sm:rounded-3xl overflow-hidden bg-[#0d1117] text-white shadow-2xl border border-slate-800 select-none">
      {/* Soft emerald background lighting */}
      <div className="absolute top-0 right-1/4 w-[300px] sm:w-[500px] h-[300px] sm:h-[500px] bg-emerald-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative min-h-[360px] sm:min-h-[440px] md:min-h-[500px] flex items-center cursor-grab active:cursor-grabbing overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.div
            key={current}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
            drag="x"
            dragConstraints={{ left: 0, right: 0 }}
            dragElastic={0.1}
            onDragEnd={handleDragEnd}
            className="w-full grid grid-cols-1 lg:grid-cols-12 items-center gap-6 sm:gap-8 px-4 sm:px-10 md:px-16 py-6 sm:py-10"
          >
            {/* Left Content */}
            <div className="lg:col-span-7 z-10 pointer-events-none text-left">
              {/* Top Accent Sub-header */}
              <div className="text-emerald-400 font-extrabold text-[11px] sm:text-xs tracking-wider uppercase mb-2 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                <span>{topBadge}</span>
              </div>

              {/* Main Headline */}
              <h1 className="text-2xl sm:text-5xl md:text-6xl font-black text-white tracking-tight mb-3 sm:mb-6 leading-tight">
                <div>{title1}</div>
                <div className="text-slate-100">{title2}</div>
              </h1>

              {/* Bright Green Pill Badge */}
              <div className="inline-block mb-3 sm:mb-6">
                <span className="px-3.5 py-1.5 sm:px-5 sm:py-2.5 rounded-full bg-[#00E676] text-slate-950 font-extrabold text-xs sm:text-base shadow-lg shadow-emerald-500/20">
                  {pillBadge}
                </span>
              </div>

              {/* Fine Details line */}
              <p className="text-slate-400 text-xs sm:text-sm font-medium tracking-wide">
                {details}
              </p>

              {/* Brand Watermark Bottom Left */}
              <div className="mt-4 sm:mt-8 flex items-center gap-2">
                <span className="text-sm sm:text-xl font-black text-white tracking-widest uppercase">
                  BAHO <span className="text-emerald-400">MARKET</span>
                </span>
              </div>
            </div>

            {/* Right Side 3D Dynamic Floating Product Showcase */}
            <div className="lg:col-span-5 relative flex justify-center items-center pointer-events-none mt-2 lg:mt-0">
              {/* Backlight Glow Effect */}
              <div className="absolute w-44 h-44 sm:w-72 sm:h-72 bg-emerald-500/20 rounded-full blur-2xl sm:blur-3xl" />

              <motion.img
                animate={{ y: [-4, 4, -4], rotate: [0, 1, 0] }}
                transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
                src={activeSlide.image}
                alt={title1}
                className="w-full max-w-[260px] sm:max-w-md lg:max-w-xl h-auto max-h-[200px] sm:max-h-[340px] lg:max-h-[420px] object-contain drop-shadow-[0_15px_30px_rgba(0,0,0,0.8)] relative z-10"
              />
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Pagination Indicator Dots at bottom center */}
      <div className="absolute bottom-5 left-1/2 -translate-x-1/2 flex items-center gap-2 z-20">
        {heroSlides.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrent(idx)}
            className={`h-2 rounded-full transition-all duration-300 ${
              current === idx ? 'w-8 bg-white' : 'w-2 bg-slate-600 hover:bg-slate-400'
            }`}
          />
        ))}
      </div>
    </section>
  )
}
