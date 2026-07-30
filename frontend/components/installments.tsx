'use client'

import { motion } from 'framer-motion'
import { CreditCard, TrendingUp, Zap } from 'lucide-react'
import { useState } from 'react'
import { useLanguage } from '@/context/language-context'

interface InstallmentPlan {
  months: number
  rate: number
  description: string
}

const plans: InstallmentPlan[] = [
  { months: 3, rate: 0, description: '0%' },
  { months: 6, rate: 0, description: '0%' },
  { months: 12, rate: 2, description: '2%' },
]

export function Installments() {
  const [selectedPrice, setSelectedPrice] = useState(1299000)
  const [selectedMonths, setSelectedMonths] = useState(12)
  const { t } = useLanguage()

  const getMonthlyPayment = (price: number, months: number) => {
    return Math.round(price / months)
  }

  const monthlyPayment = getMonthlyPayment(selectedPrice, selectedMonths)
  const totalPayment = selectedPrice
  const totalInterest = 0

  return (
    <section className="py-12 lg:py-16 my-4 bg-slate-50 border border-slate-100 rounded-3xl p-6 sm:p-10 shadow-xs" suppressHydrationWarning>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mb-8"
      >
        <h2 className="text-2xl lg:text-3xl font-black mb-2 text-slate-900 tracking-tight">
          {t('installmentsTitle')}
        </h2>
        <p className="text-slate-500 text-sm sm:text-base">
          {t('installmentsSubtitle')}
        </p>
      </motion.div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Calculator */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-xs"
        >
          <h3 className="text-xl font-bold mb-6 text-slate-900">{t('calcTitle')}</h3>

          {/* Price Input */}
          <div className="mb-8">
            <label className="block text-xs font-extrabold uppercase text-slate-500 tracking-wider mb-3">
              {t('devicePrice')}
            </label>
            <div className="relative">
              <input
                type="range"
                min="100000"
                max="5000000"
                step="50000"
                value={selectedPrice}
                onChange={(e) => setSelectedPrice(Number(e.target.value))}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
              />
              <div className="flex justify-between text-xs text-slate-400 font-semibold mt-2">
                <span>100K {t('sum')}</span>
                <span>5M {t('sum')}</span>
              </div>
            </div>
            <div className="mt-4 text-3xl font-black text-emerald-800 tracking-tight">
              {new Intl.NumberFormat('ru-RU').format(selectedPrice)} {t('sum')}
            </div>
          </div>

          {/* Months Selection */}
          <div className="mb-8">
            <label className="block text-xs font-extrabold uppercase text-slate-500 tracking-wider mb-3">
              {t('paymentDuration')}
            </label>
            <div className="grid grid-cols-3 gap-2.5">
              {plans.map((plan) => (
                <motion.button
                  key={plan.months}
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  onClick={() => setSelectedMonths(plan.months)}
                  className={`py-3 px-2 rounded-xl font-bold transition text-xs sm:text-sm border ${
                    selectedMonths === plan.months
                      ? 'bg-emerald-800 text-white border-emerald-800 shadow-md'
                      : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'
                  }`}
                >
                  {plan.months}м
                </motion.button>
              ))}
            </div>
          </div>

          {/* Payment Breakdown */}
          <div className="bg-emerald-50/60 rounded-xl p-5 border border-emerald-100">
            <div className="flex justify-between items-center">
              <span className="text-slate-600 text-xs sm:text-sm font-semibold">{t('monthlyPaymentLabel')}</span>
              <span className="text-xl sm:text-2xl font-black text-emerald-800">
                {new Intl.NumberFormat('ru-RU').format(monthlyPayment)} {t('sum')}
              </span>
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.98 }}
            className="w-full mt-6 py-3.5 bg-emerald-800 hover:bg-emerald-900 text-white font-bold text-sm rounded-xl transition shadow-md"
          >
            {t('getPlanBtn')}
          </motion.button>
        </motion.div>

        {/* Benefits */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          className="space-y-4 flex flex-col justify-center"
        >
          {[
            {
              icon: TrendingUp,
              title: t('flexibleTermsTitle'),
              description: t('flexibleTermsDesc'),
            },
            {
              icon: Zap,
              title: t('instantApprovalTitle'),
              description: t('instantApprovalDesc'),
            },
          ].map((benefit, index) => {
            const Icon = benefit.icon
            return (
              <motion.div
                key={index}
                whileHover={{ x: 6 }}
                className="flex gap-4 p-5 bg-white border border-slate-200 rounded-2xl shadow-xs transition hover:border-emerald-300"
              >
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-emerald-50 text-emerald-800">
                    <Icon className="h-6 w-6" />
                  </div>
                </div>
                <div>
                  <h4 className="font-extrabold text-slate-900 text-sm mb-1">{benefit.title}</h4>
                  <p className="text-xs text-slate-500 font-medium leading-relaxed">
                    {benefit.description}
                  </p>
                </div>
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
