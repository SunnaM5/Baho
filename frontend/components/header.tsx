'use client'

import { useState, useRef, useEffect } from 'react'
import { Search, Heart, ShoppingCart, Globe, ChevronDown, Check, Phone, MessageCircle, Menu, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import { useLanguage } from '@/context/language-context'

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [searchFocus, setSearchFocus] = useState(false)
  const [langDropdownOpen, setLangDropdownOpen] = useState(false)
  const { lang, setLang, t } = useLanguage()

  const langRef = useRef<HTMLDivElement>(null)

  const languages = [
    { code: 'ru', label: 'Русский', flag: '🇷🇺' },
    { code: 'uz', label: "O'zbekcha", flag: '🇺🇿' },
    { code: 'en', label: 'English', flag: '🇬🇧' },
  ]

  const currentLangObj = languages.find((l) => l.code === lang) || languages[0]

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (langRef.current && !langRef.current.contains(event.target as Node)) {
        setLangDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const menuItems = [
    { key: 'all', label: t('all'), filterName: 'Все' },
    { key: 'smartphones', label: t('smartphones'), filterName: 'Смартфоны' },
    { key: 'iphones', label: t('iphones'), filterName: 'iPhones' },
    { key: 'samsung', label: t('samsung'), filterName: 'Samsung' },
    { key: 'xiaomi', label: t('xiaomi'), filterName: 'Xiaomi' },
    { key: 'laptops', label: t('laptops'), filterName: 'Ноутбуки' },
    { key: 'tablets', label: t('tablets'), filterName: 'Планшеты' },
    { key: 'headphones', label: t('headphones'), filterName: 'Наушники' },
    { key: 'accessories', label: t('accessories'), filterName: 'Аксессуары' },
  ]

  const selectCategoryAndScroll = (categoryName: string) => {
    const section = document.getElementById('catalog-section')
    if (section) {
      window.dispatchEvent(new CustomEvent('selectCategoryFilter', { detail: categoryName }))
      const yOffset = -100
      const y = section.getBoundingClientRect().top + window.pageYOffset + yOffset
      window.scrollTo({ top: y, behavior: 'smooth' })
    } else {
      window.location.href = `/catalog?category=${encodeURIComponent(categoryName)}`
    }
  }

  return (
    <>
      {/* Top Info Bar */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="hidden lg:flex items-center justify-between bg-emerald-950 text-emerald-100 px-6 py-2 text-xs border-b border-emerald-900"
      >
        <div className="flex items-center gap-8">
          <a href="tel:+998773710808" className="flex items-center gap-2 hover:text-white transition">
            <Phone className="w-3.5 h-3.5 text-emerald-400" />
            <span>+998 77 371-08-08</span>
          </a>
          <div className="flex items-center gap-2 hover:text-white cursor-pointer transition">
            <MessageCircle className="w-3.5 h-3.5 text-emerald-400" />
            <span>{t('support24')}</span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-emerald-400 font-semibold">{t('deliveryNote')}</span>
        </div>
      </motion.div>

      {/* Main Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="sticky top-0 z-50 bg-white/95 border-b border-emerald-100 backdrop-blur-lg shadow-sm"
      >
        <div className="w-full max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-2.5 sm:py-3.5">
          <div className="flex items-center justify-between gap-2 sm:gap-4">
            {/* Logo */}
            <Link href="/" className="flex-shrink-0">
              <motion.div
                whileHover={{ scale: 1.03 }}
                className="text-xl sm:text-2xl font-black tracking-tight flex items-center"
              >
                <span className="text-emerald-800">BAHO</span>
                <span className="text-emerald-600 ml-1">MARKET</span>
              </motion.div>
            </Link>

            {/* Desktop Search Bar */}
            <motion.div
              animate={{ scale: searchFocus ? 1.01 : 1 }}
              className="hidden md:flex flex-1 max-w-md mx-auto relative"
            >
              <input
                type="text"
                placeholder={t('searchPlaceholder')}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:border-emerald-600 focus:bg-white transition text-sm"
                onFocus={() => setSearchFocus(true)}
                onBlur={() => setSearchFocus(false)}
              />
              <Search className="absolute right-3 top-3 w-4 h-4 text-slate-400" />
            </motion.div>

            {/* Right Action Icons */}
            <div className="flex items-center gap-1 sm:gap-3">
              <Link href="/wishlist">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="p-2 sm:p-2.5 hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 rounded-xl transition relative min-w-[40px] min-h-[40px] flex items-center justify-center"
                  title={t('wishlist')}
                >
                  <Heart className="w-5 h-5" />
                  <span className="absolute top-0.5 right-0.5 w-4 h-4 bg-emerald-600 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                    0
                  </span>
                </motion.button>
              </Link>

              <Link href="/cart">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="p-2 sm:p-2.5 hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 rounded-xl transition relative min-w-[40px] min-h-[40px] flex items-center justify-center"
                  title={t('cart')}
                >
                  <ShoppingCart className="w-5 h-5" />
                  <span className="absolute top-0.5 right-0.5 w-4 h-4 bg-emerald-600 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                    0
                  </span>
                </motion.button>
              </Link>

              {/* Language Switcher Dropdown */}
              <div className="relative" ref={langRef}>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setLangDropdownOpen(!langDropdownOpen)}
                  className="px-2.5 py-1.5 sm:px-3 sm:py-2 bg-slate-100 hover:bg-emerald-50 text-slate-800 hover:text-emerald-800 rounded-xl transition flex items-center gap-1 text-xs font-bold border border-slate-200 min-h-[40px]"
                >
                  <Globe className="w-4 h-4 text-emerald-700" />
                  <span>{currentLangObj.code.toUpperCase()}</span>
                  <ChevronDown className={`w-3 h-3 text-slate-400 transition-transform ${langDropdownOpen ? 'rotate-180' : ''}`} />
                </motion.button>

                {/* Dropdown Menu */}
                <AnimatePresence>
                  {langDropdownOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 10, scale: 0.95 }}
                      transition={{ duration: 0.15 }}
                      className="absolute right-0 mt-2 w-40 bg-white rounded-2xl shadow-xl border border-slate-200 py-2 z-50 overflow-hidden"
                    >
                      {languages.map((l) => (
                        <button
                          key={l.code}
                          onClick={() => {
                            setLang(l.code as any)
                            setLangDropdownOpen(false)
                          }}
                          className={`w-full px-3.5 py-2 text-xs font-semibold flex items-center justify-between hover:bg-emerald-50 hover:text-emerald-800 transition ${
                            lang === l.code ? 'bg-emerald-50/80 text-emerald-800 font-extrabold' : 'text-slate-700'
                          }`}
                        >
                          <span className="flex items-center gap-2">
                            <span>{l.flag}</span>
                            <span>{l.label}</span>
                          </span>
                          {lang === l.code && <Check className="w-3.5 h-3.5 text-emerald-600" />}
                        </button>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Mobile Menu Toggle */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="lg:hidden p-2 text-slate-700 hover:bg-slate-100 rounded-xl transition min-w-[40px] min-h-[40px] flex items-center justify-center"
                aria-label="Toggle menu"
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>

          {/* Dedicated Mobile Search Row */}
          <div className="mt-2.5 md:hidden">
            <div className="relative w-full">
              <input
                type="text"
                placeholder={t('searchPlaceholder')}
                className="w-full px-3.5 py-2 rounded-xl bg-slate-100 border border-slate-200 focus:outline-none focus:border-emerald-600 focus:bg-white transition text-xs font-medium"
              />
              <Search className="absolute right-3 top-2.5 w-4 h-4 text-slate-400" />
            </div>
          </div>

          {/* Desktop Header Category Navigation Bar */}
          <motion.div
            className="hidden lg:flex items-center gap-1 overflow-x-auto pb-0.5 scrollbar-hide border-t border-slate-100 pt-2 mt-3"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {menuItems.map((item) => (
              item.key === 'all' ? (
                <Link
                  key={item.key}
                  href="/catalog"
                  className="px-3.5 py-1.5 text-xs font-bold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 transition rounded-lg flex items-center gap-1"
                >
                  {item.label}
                </Link>
              ) : (
                <button
                  key={item.key}
                  onClick={() => selectCategoryAndScroll(item.filterName)}
                  className="px-3.5 py-1.5 text-xs font-semibold text-slate-700 hover:text-emerald-700 hover:bg-emerald-50 transition rounded-lg"
                >
                  {item.label}
                </button>
              )
            ))}
          </motion.div>
        </div>

        {/* Mobile Slide-down Drawer */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="lg:hidden overflow-hidden bg-white border-t border-slate-200 shadow-xl"
            >
              <div className="px-4 py-4 space-y-1 max-h-[75vh] overflow-y-auto">
                <div className="grid grid-cols-2 gap-2 mb-3 pb-3 border-b border-slate-100">
                  <Link
                    href="/cart"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center justify-center gap-2 p-2.5 font-bold text-xs text-emerald-800 bg-emerald-50 rounded-xl border border-emerald-100"
                  >
                    <ShoppingCart className="w-4 h-4" />
                    <span>{t('cart')}</span>
                  </Link>
                  <Link
                    href="/wishlist"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center justify-center gap-2 p-2.5 font-bold text-xs text-emerald-800 bg-emerald-50 rounded-xl border border-emerald-100"
                  >
                    <Heart className="w-4 h-4" />
                    <span>{t('wishlist')}</span>
                  </Link>
                </div>

                <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 py-1">
                  {t('catalogTitle')}
                </div>
                {menuItems.map((item) => (
                  <button
                    key={item.key}
                    onClick={() => {
                      setMobileMenuOpen(false)
                      selectCategoryAndScroll(item.filterName)
                    }}
                    className="block w-full text-left px-3.5 py-2.5 text-xs font-semibold text-slate-700 hover:text-emerald-800 hover:bg-emerald-50 rounded-xl transition"
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.header>
    </>
  )
}
