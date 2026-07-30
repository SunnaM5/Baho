'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Smartphone, CheckCircle, ArrowRight, RefreshCw, Sparkles, X, Calculator, Send, Check } from 'lucide-react'
import { useLanguage } from '@/context/language-context'

export function TradeIn() {
  const { lang } = useLanguage()
  const [modalOpen, setModalOpen] = useState(false)
  const [selectedBrand, setSelectedBrand] = useState('Apple')
  const [modelName, setModelName] = useState('')
  const [condition, setCondition] = useState('ideal')
  const [phone, setPhone] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const translations = {
    ru: {
      badge: 'Программа Trade-In',
      title: 'Обменяйте старый смартфон на новый со скидкой',
      description: 'Обновитесь до нового флагманского устройства быстро и безопасно. Мы оценим ваш б/у телефон по максимальной рыночной цене.',
      step1Title: '1. Оценка вашего устройства',
      step1Desc: 'Укажите модель и состояние вашего текущего смартфона',
      step2Title: '2. Мгновенный расчёт',
      step2Desc: 'Получите точную сумму скидки на покупку нового телефона',
      step3Title: '3. Передача устройства',
      step3Desc: 'Принесите устройство в наш магазин или передайте курьеру',
      step4Title: '4. Покупка с выгодой',
      step4Desc: 'Заберите новое устройство, оплатив только разницу в цене',
      b1: 'Честная и чеклистовая оценка за 5 минут',
      b2: 'Максимальные выкупные цены в Ташкенте',
      b3: 'Безопасный перенос ваших данных со старого телефона',
      b4: 'Возможность оформления остатка в рассрочку 0%',
      btn: 'Рассчитать Trade-In',
      modalTitle: 'Онлайн расчёт Trade-In',
      modalSubtitle: 'Укажите данные вашего устройства для предварительной оценки',
      brandLabel: 'Марка смартфона',
      modelLabel: 'Модель смартфона',
      modelPlaceholder: 'Например: iPhone 13 Pro 128GB',
      conditionLabel: 'Состояние устройства',
      condIdeal: 'Идеальное (без царапин, полный комплект)',
      condGood: 'Хорошее (мелкие следы использования)',
      condUsed: 'Удовлетворительное (есть царапины/потёртости)',
      estValue: 'Примерная выкупная стоимость:',
      phoneLabel: 'Ваш номер телефона для связи',
      phonePlaceholder: '+998 90 123 45 67',
      submitBtn: 'Отправить заявку на выкуп',
      successMsg: 'Заявка успешно отправлена! Наш специалист свяжется с вами в течение 10 минут.',
    },
    uz: {
      badge: 'Trade-In Dasturi',
      title: 'Eski smartfoningizni yangisiga chegirma bilan almashtiring',
      description: 'Eski qurilmangizni tez va xavfsiz almashtiring. Biz smartfoningizni eng yuqori bozor narxida baholaymiz.',
      step1Title: '1. Qurilmangizni baholash',
      step1Desc: 'Amaldagi smartfoningizning modeli va holatini koʻrsating',
      step2Title: '2. Onlayn hisoblash',
      step2Desc: 'Yangi telefon xarid qilish uchun aniq chegirma summasini oling',
      step3Title: '3. Qurilmani topshirish',
      step3Desc: 'Qurilmani doʻkonimizga olib keling yoki kuryerga topshiring',
      step4Title: '4. Xaridni yakunlash',
      step4Desc: 'Faqatgina farqini toʻlab, yangi smartfonni olib keting',
      b1: '5 daqiqada halol va tezkor baholash',
      b2: 'Toshkentdagi eng yuqori baholash narxlari',
      b3: 'Maʼlumotlaringizni xavfsiz koʻchirish',
      b4: 'Qolgan summani 0% boʻlib toʻlash imkoniyati',
      btn: 'Trade-In narxini hisoblash',
      modalTitle: 'Trade-In onlayn hisoblash',
      modalSubtitle: 'Dastlabki baholash uchun smartfoningiz maʼlumotlarini kiriting',
      brandLabel: 'Smartfon brendi',
      modelLabel: 'Smartfon modeli',
      modelPlaceholder: 'Masalan: iPhone 13 Pro 128GB',
      conditionLabel: 'Qurilma holati',
      condIdeal: 'Aʼlo (chizilmagan, toʻliq komplekt)',
      condGood: 'Yaxshi (kichik foydalanish izlari)',
      condUsed: 'Qoniqarli (chizilgan joylari bor)',
      estValue: 'Taxminiy baholash qiymati:',
      phoneLabel: 'Bogʻlanish uchun telefon raqamingiz',
      phonePlaceholder: '+998 90 123 45 67',
      submitBtn: 'Baholash soʻrovini yuborish',
      successMsg: 'Soʻrovingiz muvaffaqiyatli yuborildi! Mutaxassisimiz 10 daqiqa ichida bogʻlanadi.',
    },
    en: {
      badge: 'Trade-In Program',
      title: 'Exchange your old smartphone for a new one',
      description: 'Upgrade to your next premium device easily and transparently. We give you the maximum market trade-in value.',
      step1Title: '1. Evaluate Your Device',
      step1Desc: 'Tell us about your current device brand and condition',
      step2Title: '2. Get Instant Quote',
      step2Desc: 'Receive a fair market discount quote immediately',
      step3Title: '3. Complete the Trade',
      step3Desc: 'Bring your device to our shop or hand it to courier',
      step4Title: '4. Enjoy Your Discount',
      step4Desc: 'Apply the credit and pay only the difference',
      b1: 'Fair assessment in just 5 minutes',
      b2: 'Top market buyout prices in Tashkent',
      b3: 'Secure data transfer from old phone',
      b4: 'Option to pay remaining amount in 0% installments',
      btn: 'Calculate Trade-In',
      modalTitle: 'Trade-In Calculator',
      modalSubtitle: 'Enter your device details for an instant trade-in quote',
      brandLabel: 'Device Brand',
      modelLabel: 'Device Model',
      modelPlaceholder: 'e.g. iPhone 13 Pro 128GB',
      conditionLabel: 'Device Condition',
      condIdeal: 'Mint (no scratches, original box)',
      condGood: 'Good (minor signs of use)',
      condUsed: 'Fair (scratches / visible wear)',
      estValue: 'Estimated Trade-In Value:',
      phoneLabel: 'Your Phone Number',
      phonePlaceholder: '+998 90 123 45 67',
      submitBtn: 'Submit Trade-In Request',
      successMsg: 'Request submitted successfully! Our expert will contact you within 10 minutes.',
    },
  }

  const t = translations[lang as keyof typeof translations] || translations.ru

  const steps = [
    { title: t.step1Title, description: t.step1Desc },
    { title: t.step2Title, description: t.step2Desc },
    { title: t.step3Title, description: t.step3Desc },
    { title: t.step4Title, description: t.step4Desc },
  ]

  const benefits = [t.b1, t.b2, t.b3, t.b4]

  const calculateEstimate = () => {
    let base = 4500000
    if (selectedBrand === 'Apple') base = 6500000
    if (selectedBrand === 'Samsung') base = 5200000
    if (selectedBrand === 'Xiaomi') base = 3200000

    if (condition === 'ideal') base *= 1.2
    if (condition === 'used') base *= 0.75

    return base.toLocaleString('ru-RU')
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(true)
    setTimeout(() => {
      setSubmitted(false)
      setModalOpen(false)
      setModelName('')
      setPhone('')
    }, 2500)
  }

  return (
    <section className="py-12 lg:py-16 my-6 bg-gradient-to-br from-emerald-950 via-emerald-900 to-slate-950 text-white rounded-3xl p-6 md:p-12 relative overflow-hidden shadow-2xl">
      {/* Background Glow */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-emerald-400/10 rounded-full blur-3xl pointer-events-none" />

      <div className="grid lg:grid-cols-12 gap-8 lg:gap-12 items-center relative z-10">
        {/* Left Side - Animated Visual Cards */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          className="lg:col-span-5 flex justify-center"
        >
          <div className="relative w-full max-w-sm h-80 sm:h-96 flex items-center justify-center">
            <motion.div
              animate={{ y: [-10, 10, -10], rotate: [-4, 4, -4] }}
              transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
              className="absolute w-52 sm:w-60 h-72 sm:h-80 bg-emerald-800/80 border border-emerald-500/30 backdrop-blur-xl rounded-3xl shadow-2xl p-6 flex flex-col justify-between -left-2 sm:left-2"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-emerald-300 uppercase">Старый телефон</span>
                <RefreshCw className="w-5 h-5 text-emerald-400" />
              </div>
              <div className="my-auto text-center">
                <Smartphone className="w-16 h-16 mx-auto text-emerald-200/50 mb-2" />
                <span className="text-sm font-bold text-emerald-100">Выкупная цена</span>
                <p className="text-xl font-black text-white mt-1">до 8,500,000 сум</p>
              </div>
            </motion.div>

            <motion.div
              animate={{ y: [10, -10, 10], rotate: [4, -4, 4] }}
              transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut', delay: 0.5 }}
              className="absolute w-52 sm:w-60 h-72 sm:h-80 bg-white/10 border border-white/20 backdrop-blur-xl rounded-3xl shadow-2xl p-6 flex flex-col justify-between -right-2 sm:right-2 top-8"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white uppercase">Новый флагман</span>
                <Sparkles className="w-5 h-5 text-amber-400" />
              </div>
              <div className="my-auto text-center">
                <Smartphone className="w-16 h-16 mx-auto text-emerald-400 mb-2" />
                <span className="text-xs font-bold text-emerald-300">Скидка за обмен</span>
                <p className="text-xl font-black text-emerald-300 mt-1">- 100% разницы</p>
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Right Side - Information */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          className="lg:col-span-7 space-y-6"
        >
          <div>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-800/80 text-emerald-300 text-xs font-bold rounded-full mb-3 border border-emerald-700/50">
              <RefreshCw className="w-3.5 h-3.5" /> {t.badge}
            </span>
            <h2 className="text-2xl sm:text-4xl font-black text-white leading-tight mb-3">
              {t.title}
            </h2>
            <p className="text-slate-300 text-sm leading-relaxed max-w-xl">
              {t.description}
            </p>
          </div>

          {/* Steps */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {steps.map((step, idx) => (
              <div key={idx} className="bg-white/5 border border-white/10 rounded-2xl p-4 backdrop-blur-sm">
                <h4 className="font-extrabold text-white text-sm mb-1">{step.title}</h4>
                <p className="text-xs text-slate-400">{step.description}</p>
              </div>
            ))}
          </div>

          {/* Benefits */}
          <div className="space-y-2 pt-2 border-t border-emerald-800/60">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-center gap-2 text-xs font-semibold text-emerald-200">
                <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span>{benefit}</span>
              </div>
            ))}
          </div>

          <button
            onClick={() => setModalOpen(true)}
            className="inline-flex items-center gap-2 px-8 py-3.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-sm rounded-xl transition-all shadow-lg hover:shadow-emerald-500/20 active:scale-95 cursor-pointer"
          >
            {t.btn}
            <ArrowRight className="w-4 h-4" />
          </button>
        </motion.div>
      </div>

      {/* Trade-In Calculator Modal */}
      <AnimatePresence>
        {modalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-slate-900 border border-emerald-500/30 rounded-3xl p-6 sm:p-8 max-w-lg w-full shadow-2xl relative text-white"
            >
              <button
                onClick={() => setModalOpen(false)}
                className="absolute top-5 right-5 p-2 rounded-full bg-white/10 hover:bg-white/20 text-slate-400 hover:text-white transition"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-emerald-500/20 rounded-2xl text-emerald-400 border border-emerald-500/30">
                  <Calculator className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-extrabold">{t.modalTitle}</h3>
                  <p className="text-xs text-slate-400">{t.modalSubtitle}</p>
                </div>
              </div>

              {submitted ? (
                <div className="py-8 text-center space-y-4">
                  <div className="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto border border-emerald-500/40">
                    <Check className="w-8 h-8" />
                  </div>
                  <p className="text-sm font-semibold text-emerald-200">{t.successMsg}</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                  {/* Brand */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                      {t.brandLabel}
                    </label>
                    <div className="grid grid-cols-4 gap-2">
                      {['Apple', 'Samsung', 'Xiaomi', 'Другой'].map((b) => (
                        <button
                          key={b}
                          type="button"
                          onClick={() => setSelectedBrand(b)}
                          className={`py-2 px-3 rounded-xl text-xs font-bold transition border ${
                            selectedBrand === b
                              ? 'bg-emerald-500 text-slate-950 border-emerald-400'
                              : 'bg-white/5 text-slate-300 border-white/10 hover:bg-white/10'
                          }`}
                        >
                          {b}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Model */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                      {t.modelLabel}
                    </label>
                    <input
                      type="text"
                      required
                      value={modelName}
                      onChange={(e) => setModelName(e.target.value)}
                      placeholder={t.modelPlaceholder}
                      className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-emerald-500 transition"
                    />
                  </div>

                  {/* Condition */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                      {t.conditionLabel}
                    </label>
                    <select
                      value={condition}
                      onChange={(e) => setCondition(e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-800 border border-white/10 text-white text-sm focus:outline-none focus:border-emerald-500 transition"
                    >
                      <option value="ideal">{t.condIdeal}</option>
                      <option value="good">{t.condGood}</option>
                      <option value="used">{t.condUsed}</option>
                    </select>
                  </div>

                  {/* Calculated Value */}
                  <div className="bg-emerald-950/80 border border-emerald-500/40 rounded-2xl p-4 text-center">
                    <span className="text-xs text-emerald-300 font-semibold">{t.estValue}</span>
                    <p className="text-2xl font-black text-emerald-400 mt-0.5">
                      ~ {calculateEstimate()} сум
                    </p>
                  </div>

                  {/* Phone */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                      {t.phoneLabel}
                    </label>
                    <input
                      type="tel"
                      required
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder={t.phonePlaceholder}
                      className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-emerald-500 transition"
                    />
                  </div>

                  <button
                    type="submit"
                    className="w-full py-3.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-sm rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20"
                  >
                    <Send className="w-4 h-4" />
                    {t.submitBtn}
                  </button>
                </form>
              )}
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </section>
  )
}
