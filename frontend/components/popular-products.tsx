'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ProductCard } from './product-card'
import { ApiService } from '@/lib/api'
import { useLanguage } from '@/context/language-context'

export function PopularProducts() {
  const [products, setProducts] = useState<any[]>([])
  const [activeCategory, setActiveCategory] = useState<string>('Все')
  const [loading, setLoading] = useState(true)
  const { t } = useLanguage()

  // Products are fetched directly from Django Admin API
  const defaultProducts: any[] = []

  useEffect(() => {
    ApiService.getProducts()
      .then((prodRes) => {
        const prodList = Array.isArray(prodRes) ? prodRes : prodRes.results || []
        setProducts(prodList)
      })
      .catch((err) => {
        console.error('Failed to load catalog products from API:', err)
        setProducts([])
      })
      .finally(() => setLoading(false))

    // Listen for custom category filter selection events triggered from Header navigation links
    const handleCategoryFilterEvent = (e: any) => {
      if (e.detail) {
        setActiveCategory(e.detail)
      }
    }
    window.addEventListener('selectCategoryFilter', handleCategoryFilterEvent)

    return () => {
      window.removeEventListener('selectCategoryFilter', handleCategoryFilterEvent)
    }
  }, [])

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  // Active products data set
  const allProducts = products.length > 0 ? products : defaultProducts

  // Flexible matching logic ensuring all items are displayed
  const filteredProducts = activeCategory === 'Все'
    ? allProducts
    : allProducts.filter(p => {
        const catName = (typeof p.category === 'object' ? p.category?.name : p.category) || ''
        const brandName = (typeof p.brand === 'object' ? p.brand?.name : p.brand) || ''
        const prodName = p.name || ''
        const searchTarget = activeCategory.toLowerCase()

        if (searchTarget === 'iphones' || searchTarget === 'iphone') {
          return prodName.toLowerCase().includes('iphone') || catName.toLowerCase().includes('iphone') || brandName.toLowerCase().includes('apple')
        }
        if (searchTarget === 'samsung') {
          return prodName.toLowerCase().includes('samsung') || catName.toLowerCase().includes('samsung') || brandName.toLowerCase().includes('samsung')
        }
        if (searchTarget === 'xiaomi') {
          return prodName.toLowerCase().includes('xiaomi') || catName.toLowerCase().includes('xiaomi') || brandName.toLowerCase().includes('xiaomi')
        }
        if (searchTarget === 'смартфоны' || searchTarget === 'smartphones') {
          return (
            prodName.toLowerCase().includes('iphone') ||
            prodName.toLowerCase().includes('samsung') ||
            prodName.toLowerCase().includes('xiaomi') ||
            catName.toLowerCase().includes('смартфон')
          )
        }

        return (
          catName.toLowerCase().includes(searchTarget) ||
          brandName.toLowerCase().includes(searchTarget) ||
          prodName.toLowerCase().includes(searchTarget)
        )
      })

  if (loading) {
    return <div className="py-16 text-center text-slate-500 font-medium">{t('loadingCatalog')}</div>
  }

  return (
    <section id="catalog-section" className="py-8 lg:py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
      >
        <div>
          <h2 className="text-2xl lg:text-3xl font-black text-slate-900 mb-1">
            {t('catalogTitle')}
          </h2>
          <p className="text-slate-500 text-sm">
            {t('catalogDesc')}
          </p>
        </div>

        {activeCategory !== 'Все' && (
          <button
            onClick={() => setActiveCategory('Все')}
            className="self-start sm:self-auto text-xs font-bold text-emerald-700 hover:text-emerald-900 bg-emerald-50 hover:bg-emerald-100 px-3.5 py-2 rounded-xl transition"
          >
            {t('showAllProducts')}
          </button>
        )}
      </motion.div>

      {/* Products Grid */}
      {filteredProducts.length === 0 ? (
        <div className="py-16 text-center bg-white rounded-3xl border border-slate-200 p-8 shadow-xs">
          <p className="text-slate-500 font-medium text-sm mb-4">
            {t('noProductsFound')}
          </p>
          <button
            onClick={() => setActiveCategory('Все')}
            className="px-6 py-2.5 bg-emerald-800 text-white text-xs font-bold rounded-xl shadow-md hover:bg-emerald-900 transition"
          >
            {t('showAllProducts')}
          </button>
        </div>
      ) : (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6"
        >
          {filteredProducts.slice(0, 12).map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </motion.div>
      )}
    </section>
  )
}
