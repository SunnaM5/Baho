'use client'

import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { MapPin, Phone, Clock, Navigation } from 'lucide-react'

export default function BranchesPage() {
  const branches = [
    {
      id: 1,
      name: 'BAHO MARKET — Главный филиал (Навои)',
      address: 'г. Ташкент, Шайхантахурский р-н, ул. Алишера Навои, ст. м. Навои',
      phone: '+998 77 371-08-08',
      hours: '09:00 - 20:00 (без выходных)',
      mapUrl: 'https://yandex.ru/maps/-/CDuWMB6b',
    },
    {
      id: 2,
      name: 'BAHO MARKET — Шоурум (Чиланзар)',
      address: 'г. Ташкент, Чиланзарский р-н, м. Чиланзар, торговый центр',
      phone: '+998 77 371-08-08',
      hours: '09:00 - 20:00 (без выходных)',
      mapUrl: 'https://yandex.ru/maps/-/CDuWMB6b',
    },
  ]

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Header />
      
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h1 className="text-3xl sm:text-4xl font-black text-slate-900 mb-2">Наши Филиалы</h1>
          <p className="text-slate-600 text-sm sm:text-base">
            Посетите наши фирменные магазины BAHO MARKET, чтобы лично ознакомиться с техникой и оформить покупку или рассрочку.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {branches.map((branch) => (
            <div key={branch.id} className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-700">
                    <MapPin className="w-5 h-5" />
                  </div>
                  <h3 className="font-extrabold text-lg text-slate-900">{branch.name}</h3>
                </div>

                <div className="space-y-3.5 text-sm text-slate-600 mb-6">
                  <div className="flex items-start gap-3">
                    <MapPin className="w-4 h-4 text-emerald-600 mt-1 flex-shrink-0" />
                    <span>{branch.address}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Phone className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                    <a href={`tel:${branch.phone}`} className="font-bold text-slate-900 hover:text-emerald-700">
                      {branch.phone}
                    </a>
                  </div>
                  <div className="flex items-center gap-3">
                    <Clock className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                    <span>{branch.hours}</span>
                  </div>
                </div>
              </div>

              <a
                href={branch.mapUrl}
                target="_blank"
                rel="noreferrer"
                className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl flex items-center justify-center gap-2 transition"
              >
                <Navigation className="w-4 h-4" />
                <span>Открыть на карте</span>
              </a>
            </div>
          ))}
        </div>
      </main>

      <Footer />
    </div>
  )
}
