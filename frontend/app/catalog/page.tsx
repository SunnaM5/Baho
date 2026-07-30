'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { ProductCard } from '@/components/product-card'
import { ApiService } from '@/lib/api'
import { useLanguage } from '@/context/language-context'
import { Filter, SlidersHorizontal, ArrowUpDown, ChevronRight } from 'lucide-react'

export default function CatalogPage() {
  const { t } = useLanguage()
  const [products, setProducts] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [activeCategory, setActiveCategory] = useState<string>('Все')
  const [sortBy, setSortBy] = useState<'popular' | 'price-asc' | 'price-desc'>('popular')
  const [priceRange, setPriceRange] = useState<number>(35000000)



  const categoriesList = [
    'Все',
    'Смартфоны',
    'iPhones',
    'Samsung',
    'Xiaomi',
    'Ноутбуки',
    'Планшеты',
    'Наушники',
    'Аксессуары',
  ]

  useEffect(() => {
    ApiService.getProducts()
      .then((res) => {
        const list = Array.isArray(res) ? res : res.results || []
        setProducts(list)
      })
      .catch(() => setProducts([]))
      .finally(() => setLoading(false))
  }, [])

  const allItems = products

  // Filter products by category and max price
  let filtered = allItems.filter((p) => {
    const pPrice = Number(p.price) || 0
    if (pPrice > priceRange) return false

    if (activeCategory === 'Все') return true

    const catName = (typeof p.category === 'object' ? p.category?.name : p.category) || ''
    const brandName = (typeof p.brand === 'object' ? p.brand?.name : p.brand) || ''
    const prodName = p.name || ''
    const target = activeCategory.toLowerCase()

    if (target === 'iphones' || target === 'iphone') {
      return prodName.toLowerCase().includes('iphone') || catName.toLowerCase().includes('iphone') || brandName.toLowerCase().includes('apple')
    }
    if (target === 'samsung') {
      return prodName.toLowerCase().includes('samsung') || catName.toLowerCase().includes('samsung') || brandName.toLowerCase().includes('samsung')
    }
    if (target === 'xiaomi') {
      return prodName.toLowerCase().includes('xiaomi') || catName.toLowerCase().includes('xiaomi') || brandName.toLowerCase().includes('xiaomi')
    }
    if (target === 'смартфоны') {
      return (
        prodName.toLowerCase().includes('iphone') ||
        prodName.toLowerCase().includes('samsung') ||
        prodName.toLowerCase().includes('xiaomi') ||
        catName.toLowerCase().includes('смартфон')
      )
    }

    return (
      catName.toLowerCase().includes(target) ||
      brandName.toLowerCase().includes(target) ||
      prodName.toLowerCase().includes(target)
    )
  })

  // Sort products
  if (sortBy === 'price-asc') {
    filtered = [...filtered].sort((a, b) => Number(a.price) - Number(b.price))
  } else if (sortBy === 'price-desc') {
    filtered = [...filtered].sort((a, b) => Number(b.price) - Number(a.price))
  }

  return (
    <>
      <Header />
      <main className="min-h-screen bg-slate-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Breadcrumb Navigation */}
          <nav className="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-6">
            <Link href="/" className="hover:text-emerald-600 transition">
              Главная
            </Link>
            <ChevronRight className="w-3.5 h-3.5" />
            <span className="text-slate-900 font-bold">Каталог товаров</span>
          </nav>

          {/* Page Title Header */}
          <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm">
            <div>
              <h1 className="text-3xl font-black text-slate-900 tracking-tight">Каталог электроники</h1>
              <p className="text-slate-500 text-sm mt-1">
                Все оригинальные устройства Apple, Samsung, Xiaomi и аксессуары с официальной гарантией
              </p>
            </div>
            <div className="flex items-center gap-2 text-xs font-bold text-slate-600 bg-slate-100 px-4 py-2.5 rounded-2xl w-fit">
              Найдено товаров: <span className="text-emerald-600 text-sm font-black">{filtered.length}</span>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Sidebar Categories & Filters */}
            <aside className="lg:col-span-3 space-y-6">
              {/* Category Filter Box */}
              <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm">
                <div className="flex items-center gap-2 font-black text-slate-900 text-lg mb-4">
                  <Filter className="w-5 h-5 text-emerald-600" />
                  <span>Категории</span>
                </div>
                <div className="space-y-1.5">
                  {categoriesList.map((cat) => {
                    const isActive = activeCategory === cat
                    return (
                      <button
                        key={cat}
                        onClick={() => setActiveCategory(cat)}
                        className={`w-full text-left px-4 py-2.5 rounded-xl font-bold text-xs transition flex items-center justify-between ${
                          isActive
                            ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/20'
                            : 'text-slate-700 hover:bg-slate-100'
                        }`}
                      >
                        <span>{cat}</span>
                        {isActive && <ChevronRight className="w-4 h-4" />}
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* Price Range Filter */}
              <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-sm">
                <div className="flex items-center gap-2 font-black text-slate-900 text-base mb-4">
                  <SlidersHorizontal className="w-4 h-4 text-emerald-600" />
                  <span>Макс. цена</span>
                </div>
                <input
                  type="range"
                  min="5000000"
                  max="40000000"
                  step="1000000"
                  value={priceRange}
                  onChange={(e) => setPriceRange(Number(e.target.value))}
                  className="w-full accent-emerald-600 cursor-pointer"
                />
                <div className="flex items-center justify-between text-xs font-bold text-slate-600 mt-3">
                  <span>До:</span>
                  <span className="text-emerald-700 font-extrabold text-sm">
                    {priceRange.toLocaleString('ru-RU')} сум
                  </span>
                </div>
              </div>
            </aside>

            {/* Catalog Grid Area */}
            <section className="lg:col-span-9 space-y-6">
              {/* Controls bar */}
              <div className="bg-white px-6 py-4 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="text-xs font-bold text-slate-500 flex items-center gap-2">
                  <ArrowUpDown className="w-4 h-4 text-emerald-600" />
                  <span>Сортировка:</span>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setSortBy('popular')}
                    className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition ${
                      sortBy === 'popular'
                        ? 'bg-slate-900 text-white'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    По популярности
                  </button>
                  <button
                    onClick={() => setSortBy('price-asc')}
                    className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition ${
                      sortBy === 'price-asc'
                        ? 'bg-slate-900 text-white'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    Сначала дешевле
                  </button>
                  <button
                    onClick={() => setSortBy('price-desc')}
                    className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition ${
                      sortBy === 'price-desc'
                        ? 'bg-slate-900 text-white'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    Сначала дороже
                  </button>
                </div>
              </div>

              {/* Grid of Product Cards */}
              {loading ? (
                <div className="py-20 text-center text-slate-500 font-bold">Загрузка каталога...</div>
              ) : filtered.length === 0 ? (
                <div className="bg-white p-12 rounded-3xl border border-slate-200 text-center space-y-4">
                  <div className="text-4xl">🔍</div>
                  <h3 className="text-lg font-black text-slate-900">Товары не найдены</h3>
                  <p className="text-slate-500 text-xs max-w-xs mx-auto">
                    Попробуйте изменить параметры фильтрации или выберите другую категорию
                  </p>
                  <button
                    onClick={() => {
                      setActiveCategory('Все')
                      setPriceRange(40000000)
                    }}
                    className="px-5 py-2.5 bg-emerald-600 text-white rounded-xl font-bold text-xs shadow-md shadow-emerald-600/20 hover:bg-emerald-700 transition"
                  >
                    Сбросить фильтры
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filtered.map((product) => (
                    <ProductCard key={product.id} product={product} />
                  ))}
                </div>
              )}
            </section>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
