'use client'

import { useState, useEffect } from 'react'
import { ApiService } from '@/lib/api'
import { useLanguage } from '@/context/language-context'

export function Categories() {
  const [categories, setCategories] = useState<any[]>([])
  const { t } = useLanguage()

  useEffect(() => {
    ApiService.getCategories()
      .then((res) => {
        const list = Array.isArray(res) ? res : res.results || []
        setCategories(list)
      })
      .catch((err) => console.error('Failed to load categories:', err))
  }, [])

  // Default rich fallback categories with high-end device images
  const defaultCategories = [
    {
      id: '1',
      name: 'MacBook',
      filter: 'Ноутбуки',
      image: '/cat_macbook_tight.png',
    },
    {
      id: '2',
      name: 'iPhone',
      filter: 'iPhones',
      image: '/cat_iphone_tight.png',
    },
    {
      id: '3',
      name: 'iPad',
      filter: 'Планшеты',
      image: '/cat_ipad_tight.png',
    },
    {
      id: '4',
      name: 'Smart Watch',
      filter: 'Аксессуары',
      image: '/cat_watch_tight.png',
    },
    {
      id: '5',
      name: 'AirPods',
      filter: 'Наушники',
      image: '/cat_airpods_tight.png',
    },
    {
      id: '6',
      name: 'Samsung',
      filter: 'Samsung',
      image: '/cat_samsung.png',
    },
  ]

  const displayCategories = categories.length > 0
    ? categories.map((cat, i) => {
        const fallback = defaultCategories[i % defaultCategories.length]
        const catImg = cat.image || cat.icon
        const isValidRemote = catImg && typeof catImg === 'string' && catImg.trim() !== ''
        return {
          id: cat.id || String(i),
          name: cat.name || fallback.name,
          filter: cat.name || fallback.filter,
          image: isValidRemote ? catImg : fallback.image,
        }
      })
    : defaultCategories

  // Duplicate items 4x for a seamless, continuous infinite loop moving left to right
  const tickerItems = [...displayCategories, ...displayCategories, ...displayCategories, ...displayCategories]

  const scrollToCatalogCategory = (filterName: string) => {
    window.dispatchEvent(new CustomEvent('selectCategoryFilter', { detail: filterName }))
    const section = document.getElementById('catalog-section')
    if (section) {
      const yOffset = -90
      const y = section.getBoundingClientRect().top + window.pageYOffset + yOffset
      window.scrollTo({ top: y, behavior: 'smooth' })
    }
  }

  return (
    <section className="py-4 my-2 overflow-hidden relative w-full select-none">
      {/* Infinite marquee animation: Left to Right */}
      <style jsx>{`
        @keyframes categoryMarqueeLeftToRight {
          0% {
            transform: translateX(-50%);
          }
          100% {
            transform: translateX(0%);
          }
        }
        .animate-category-marquee {
          display: flex;
          width: max-content;
          animation: categoryMarqueeLeftToRight 30s linear infinite;
        }
        @media (hover: hover) and (pointer: fine) {
          .animate-category-marquee:hover {
            animation-play-state: paused;
          }
        }
        @media (prefers-reduced-motion: reduce) {
          .animate-category-marquee {
            animation: none;
          }
        }
        .no-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .no-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>

      {/* Smooth gradient edge masks */}
      <div className="absolute left-0 top-0 bottom-0 w-12 sm:w-20 z-10 bg-gradient-to-r from-white via-white/80 to-transparent pointer-events-none" />
      <div className="absolute right-0 top-0 bottom-0 w-12 sm:w-20 z-10 bg-gradient-to-l from-white via-white/80 to-transparent pointer-events-none" />

      {/* Section Title */}
      <div className="mb-4 px-1">
        <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
          {t('categoriesTitle')}
        </h2>
      </div>

      {/* Infinite Marquee Carousel track moving Left -> Right */}
      <div className="overflow-x-auto no-scrollbar py-2">
        <div className="animate-category-marquee flex items-center gap-3.5 sm:gap-5">
          {tickerItems.map((category, idx) => (
            <div
              key={`${category.id}-${idx}`}
              onClick={() => scrollToCatalogCategory(category.filter)}
              aria-label={category.name}
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  scrollToCatalogCategory(category.filter)
                }
              }}
              className="flex-shrink-0 w-36 sm:w-48 lg:w-52 h-36 sm:h-44 bg-white rounded-2xl p-3 border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-emerald-500/80 hover:scale-[1.04] transition-all duration-300 cursor-pointer flex flex-col justify-between items-center group text-center"
            >
              {/* Image wrapper */}
              <div className="w-full h-24 sm:h-30 flex items-center justify-center overflow-hidden pt-1">
                <img
                  src={category.image}
                  alt={category.name}
                  className="max-h-full max-w-full object-contain mix-blend-multiply group-hover:scale-108 transition-transform duration-300 drop-shadow-sm"
                />
              </div>
              {/* Category Name */}
              <span className="text-xs sm:text-sm font-semibold text-slate-800 group-hover:text-emerald-700 transition-colors truncate w-full pt-1">
                {category.name}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
