'use client'

import { motion } from 'framer-motion'
import { ShieldCheck, Truck, Zap, RefreshCw } from 'lucide-react'
import { useLanguage } from '@/context/language-context'

export function WhyUs() {
  const { t } = useLanguage()

  const features = [
    {
      icon: Zap,
      title: t('installmentBadge'),
      description: t('installmentText'),
    },
    {
      icon: ShieldCheck,
      title: t('originalBadge'),
      description: t('originalText'),
    },
    {
      icon: ShieldCheck,
      title: '100% Безопасно',
      description: 'Официальная прозрачная покупка и кассовый чек к каждому товару',
    },
    {
      icon: RefreshCw,
      title: t('tradeIn'),
      description: t('tradeInText'),
    },
  ]

  return (
    <section className="py-8 my-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {features.map((feature, index) => {
          const Icon = feature.icon
          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -4 }}
              className="p-5 bg-emerald-50/50 hover:bg-emerald-50 border border-emerald-200/60 rounded-2xl transition flex items-start gap-4"
            >
              <div className="p-3 bg-emerald-800 text-white rounded-xl flex-shrink-0 shadow-sm">
                <Icon className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-extrabold text-slate-900 text-sm mb-1 leading-snug">
                  {feature.title}
                </h3>
                <p className="text-xs text-slate-500 leading-relaxed font-medium">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          )
        })}
      </div>
    </section>
  )
}
