'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { Phone, Send, Home, MapPin, CreditCard, Truck, RefreshCw, Mail, Camera } from 'lucide-react'
import { useLanguage } from '@/context/language-context'

export function Footer() {
  const { lang, t } = useLanguage()

  const catalogItems = [
    { name: t('iphones'), filter: 'iPhones' },
    { name: t('laptops'), filter: 'Ноутбуки' },
    { name: t('tablets'), filter: 'Планшеты' },
    { name: t('samsung'), filter: 'Samsung' },
    { name: t('xiaomi'), filter: 'Xiaomi' },
  ]

  const companyItems = [
    { name: t('aboutUs'), icon: Home, href: '/about' },
    { name: t('branches'), icon: MapPin, href: '/branches' },
    { name: t('installmentsMenu'), icon: CreditCard, href: '/installments' },
  ]

  const handleCompanyClick = (action: string) => {
    if (action === 'installments') {
      const section = document.getElementById('installments-section')
      if (section) {
        section.scrollIntoView({ behavior: 'smooth' })
      } else {
        window.location.href = '/#installments-section'
      }
    } else if (action === 'about') {
      alert('BAHO MARKET — Премиальный магазин оригинальной техники и гаджетов Apple, Samsung и мультибренда в Узбекистане. Гарантия качества, выгодная рассрочка и лучший сервис!')
    } else if (action === 'branches') {
      alert('Филиалы BAHO MARKET:\n📍 г. Ташкент, ориентир: ст. м. Навои\n📞 Телефон: +998 77 371-08-08\n⏰ График работы: 09:00 - 20:00 без выходных')
    }
  }

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
    <footer className="bg-white border-t border-slate-200 text-slate-700 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
          {/* Col 1: Brand & Slogan */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <div className="flex items-center text-2xl font-black tracking-tight mb-3">
              <span className="text-emerald-800">BAHO</span>
              <span className="text-emerald-600 ml-1">MARKET</span>
            </div>
            <p className="text-slate-500 text-sm leading-relaxed max-w-xs">
              {t('footerSlogan')}
            </p>
          </motion.div>

          {/* Col 2: Catalog Links */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
          >
            <h4 className="font-extrabold text-slate-900 text-sm mb-4 uppercase tracking-wider">
              {t('footerCatalog')}
            </h4>
            <ul className="space-y-2.5 text-sm">
              {catalogItems.map((item) => (
                <li key={item.name}>
                  <button
                    onClick={() => scrollToCatalogCategory(item.filter)}
                    className="text-slate-500 hover:text-emerald-700 font-medium transition"
                  >
                    {item.name}
                  </button>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Col 3: Company Info */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <h4 className="font-extrabold text-slate-900 text-sm mb-4 uppercase tracking-wider">
              {t('footerCompany')}
            </h4>
            <ul className="space-y-2.5 text-sm">
              {companyItems.map((item) => {
                const Icon = item.icon
                return (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className="flex items-center gap-2 text-slate-500 hover:text-emerald-700 font-medium transition cursor-pointer"
                    >
                      <Icon className="w-4 h-4 text-emerald-600" />
                      <span>{item.name}</span>
                    </Link>
                  </li>
                )
              })}
            </ul>
          </motion.div>

          {/* Col 4: Contacts & Social Links */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3 }}
          >
            <h4 className="font-extrabold text-slate-900 text-sm mb-4 uppercase tracking-wider">
              {t('footerContacts')}
            </h4>
            <div className="space-y-3.5 text-sm">
              <a
                href="tel:+998773710808"
                className="flex items-center gap-2.5 text-slate-800 hover:text-emerald-700 font-bold transition"
              >
                <Phone className="w-4 h-4 text-emerald-600" />
                <span>+998 77 371-08-08</span>
              </a>

              <a
                href="https://www.instagram.com/baho_market?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2.5 text-slate-600 hover:text-pink-600 font-medium transition"
              >
                <Camera className="w-4 h-4 text-pink-600" />
                <span>@baho_market (Instagram)</span>
              </a>

              <a
                href="https://t.me/baho_market"
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2.5 text-slate-600 hover:text-sky-600 font-medium transition"
              >
                <Send className="w-4 h-4 text-sky-500" />
                <span>@baho_market (Telegram)</span>
              </a>
            </div>
          </motion.div>
        </div>

        {/* Bottom Copyright */}
        <div className="mt-12 pt-8 border-t border-slate-200 text-center">
          <p className="text-xs text-slate-400 font-medium">
            &copy; {new Date().getFullYear()} BAHO MARKET. {t('rightsReserved')}
          </p>
        </div>
      </div>

      {/* Floating Action Buttons on the bottom right */}
      <div className="fixed right-5 bottom-6 z-50 flex flex-col gap-3">
        {/* Phone Call */}
        <motion.a
          whileHover={{ scale: 1.15 }}
          whileTap={{ scale: 0.95 }}
          href="tel:+998773710808"
          className="w-12 h-12 bg-slate-900 hover:bg-emerald-700 text-white rounded-full flex items-center justify-center shadow-xl transition-all"
          title={t('callUs')}
        >
          <Phone className="w-5 h-5" />
        </motion.a>

        {/* Telegram Chat */}
        <motion.a
          whileHover={{ scale: 1.15 }}
          whileTap={{ scale: 0.95 }}
          href="https://t.me/baho_market"
          target="_blank"
          rel="noreferrer"
          className="w-12 h-12 bg-slate-900 hover:bg-sky-600 text-white rounded-full flex items-center justify-center shadow-xl transition-all"
          title="Telegram"
        >
          <Send className="w-5 h-5" />
        </motion.a>

        {/* Instagram Direct Button */}
        <motion.a
          whileHover={{ scale: 1.15 }}
          whileTap={{ scale: 0.95 }}
          href="https://www.instagram.com/baho_market?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
          target="_blank"
          rel="noreferrer"
          className="w-12 h-12 bg-slate-900 hover:bg-pink-600 text-white rounded-full flex items-center justify-center shadow-xl transition-all"
          title="Instagram"
        >
          <Camera className="w-5 h-5" />
        </motion.a>
      </div>
    </footer>
  )
}
