'use client'

import { useState } from 'react'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { CreditCard, CheckCircle2, ShieldCheck, Calculator } from 'lucide-react'
import { useLanguage } from '@/context/language-context'

export default function InstallmentsPage() {
  const [months, setMonths] = useState(12)
  const [price, setPrice] = useState(12000000)
  const { t } = useLanguage()

  const monthlyPayment = Math.round((price * 1.15) / months)

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Header />
      
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <span className="bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full border border-emerald-300 mb-3 inline-block">
            {t('flexibleTermsTitle')}
          </span>
          <h1 className="text-3xl sm:text-5xl font-black text-slate-900 mb-4">
            {t('installmentsTitle')}
          </h1>
          <p className="text-slate-600 text-base sm:text-lg">
            {t('installmentsSubtitle')}
          </p>
        </div>

        {/* Interactive Calculator */}
        <section className="bg-white rounded-3xl p-6 sm:p-10 border border-slate-200 shadow-xl mb-12 max-w-4xl mx-auto">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-700">
              <Calculator className="w-5 h-5" />
            </div>
            <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900">{t('calcTitle')}</h2>
          </div>

          <div className="space-y-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="font-bold text-slate-700 text-sm">{t('devicePrice')} ({t('sum')}):</label>
                <span className="text-lg font-black text-emerald-800">{price.toLocaleString()} {t('sum')}</span>
              </div>
              <input
                type="range"
                min={2000000}
                max={30000000}
                step={500000}
                value={price}
                onChange={(e) => setPrice(Number(e.target.value))}
                className="w-full accent-emerald-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 text-sm mb-3">{t('paymentDuration')}:</label>
              <div className="grid grid-cols-3 gap-3">
                {[3, 6, 12].map((m) => (
                  <button
                    key={m}
                    onClick={() => setMonths(m)}
                    className={`py-3 rounded-xl font-extrabold text-sm border transition ${
                      months === m
                        ? 'bg-emerald-700 text-white border-emerald-700 shadow-md'
                        : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-emerald-50'
                    }`}
                  >
                    {m} {t('monthSuffix')}
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-emerald-50 rounded-2xl p-6 border border-emerald-200 flex flex-col sm:flex-row items-center justify-between gap-4 mt-8">
              <div>
                <span className="text-xs text-slate-500 font-bold uppercase tracking-wider block mb-1">
                  {t('monthlyPaymentLabel')}
                </span>
                <span className="text-3xl font-black text-emerald-800">
                  {monthlyPayment.toLocaleString()} {t('sum')} / {t('monthSuffix')}
                </span>
              </div>
              <a
                href="/catalog"
                className="w-full sm:w-auto px-8 py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl text-center shadow-lg transition"
              >
                {t('chooseProductsBtn')}
              </a>
            </div>
          </div>
        </section>

        {/* Requirements */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <CheckCircle2 className="w-8 h-8 text-emerald-600 mb-3" />
            <h3 className="font-bold text-lg text-slate-900 mb-2">{t('zeroInterestTitle')}</h3>
            <p className="text-slate-600 text-sm">{t('zeroInterestDesc')}</p>
          </div>
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <ShieldCheck className="w-8 h-8 text-emerald-600 mb-3" />
            <h3 className="font-bold text-lg text-slate-900 mb-2">{t('flexibleTermsTitle')}</h3>
            <p className="text-slate-600 text-sm">{t('flexibleTermsDesc')}</p>
          </div>
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <CreditCard className="w-8 h-8 text-emerald-600 mb-3" />
            <h3 className="font-bold text-lg text-slate-900 mb-2">{t('instantApprovalTitle')}</h3>
            <p className="text-slate-600 text-sm">{t('instantApprovalDesc')}</p>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}
