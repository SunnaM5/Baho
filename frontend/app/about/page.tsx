'use client'

import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { ShieldCheck, Award, ThumbsUp, Clock, MapPin, Phone, Mail, Send, Camera } from 'lucide-react'
import { motion } from 'framer-motion'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Header />
      
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-emerald-900 to-slate-900 text-white rounded-3xl p-8 sm:p-12 mb-12 shadow-xl relative overflow-hidden">
          <div className="relative z-10 max-w-2xl">
            <span className="bg-emerald-500/20 text-emerald-300 text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full border border-emerald-400/30 mb-4 inline-block">
              О магазине BAHO MARKET
            </span>
            <h1 className="text-3xl sm:text-5xl font-black mb-4 leading-tight">
              Премиальная техника Apple и Samsung в Узбекистане
            </h1>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-6">
              BAHO MARKET — ведущий интернет-магазин оригинальной электроники, смартфонов, ноутбуков и аксессуаров. Мы предлагаем 100% оригинальную продукцию с официальной гарантией и лучшим обслуживанием.
            </p>
          </div>
        </section>

        {/* Advantages */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition">
            <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-700 mb-4">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">100% Оригинал & Гарантия</h3>
            <p className="text-slate-600 text-sm">
              Вся продукция поставляется от официальных дистрибьюторов. Предоставляется официальный гарантийный талон.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition">
            <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-700 mb-4">
              <Award className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Выгодная Рассрочка</h3>
            <p className="text-slate-600 text-sm">
              Быстрое оформление рассрочки от 3 до 36 месяцев без лишних справках и скрытых комиссий.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition">
            <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-700 mb-4">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Безопасная покупка</h3>
            <p className="text-slate-600 text-sm">
              Полная юридическая прозрачность, чеки и 100% защита интересов каждого клиента.
            </p>
          </div>
        </section>

        {/* Story Section */}
        <section className="bg-white rounded-3xl p-8 sm:p-10 border border-slate-200 shadow-sm mb-12">
          <h2 className="text-2xl font-black text-slate-900 mb-4">Наша Миссия</h2>
          <p className="text-slate-600 text-base leading-relaxed mb-4">
            Мы стремимся сделать современные гаджеты доступными для каждого покупателя в Узбекистане. Покупая у нас, вы получаете не только первоклассную гаджет-технику, но и персональное сопровождение, консультацию по выбору и квалифицированную поддержку.
          </p>
        </section>
      </main>

      <Footer />
    </div>
  )
}
