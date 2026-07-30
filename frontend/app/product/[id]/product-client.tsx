'use client'

import { useState, useEffect, use } from 'react'
import { motion } from 'framer-motion'
import { Heart, ShoppingCart, Check, ShieldCheck, Truck, RefreshCw, Zap, Calculator, PhoneCall, Sparkles } from 'lucide-react'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { ApiService } from '@/lib/api'
import { useLanguage } from '@/context/language-context'
import Link from 'next/link'

export function ProductPageClient({ productId }: { productId: string }) {
  const { lang, t } = useLanguage()
  const [product, setProduct] = useState<any>(null)
  const [quantity, setQuantity] = useState(1)
  const [isWishlisted, setIsWishlisted] = useState(false)
  const [isAdded, setIsAdded] = useState(false)
  const [loading, setLoading] = useState(true)

  // Interactive Product Configuration States
  const [selectedColorObj, setSelectedColorObj] = useState<any>(null)
  const [selectedStorageObj, setSelectedStorageObj] = useState<any>(null)
  const [selectedSimObj, setSelectedSimObj] = useState<any>(null)
  const [selectedMonths, setSelectedMonths] = useState<number>(12)
  const [activeImageIndex, setActiveImageIndex] = useState<number>(0)
  const [orderModalOpen, setOrderModalOpen] = useState(false)
  const [customerPhone, setCustomerPhone] = useState('')
  const [customerName, setCustomerName] = useState('')
  const [orderSuccess, setOrderSuccess] = useState(false)

  const installmentMonths = [
    { months: 3, markup: 1.0 },
    { months: 6, markup: 1.0 },
    { months: 12, markup: 1.0 },
  ]

  useEffect(() => {
    const initSelection = (data: any) => {
      setProduct(data)
      const vars = data?.variants || []
      const activeVar = vars.find((v: any) => v.is_active && v.stock > 0) || vars[0]
      if (activeVar) {
        if (data?.colors) setSelectedColorObj(data.colors.find((c: any) => c.id === activeVar.color_id) || data.colors[0])
        if (data?.memory_variants) setSelectedStorageObj(data.memory_variants.find((m: any) => m.id === activeVar.memory_id) || data.memory_variants[0])
        if (data?.sim_variants) setSelectedSimObj(data.sim_variants.find((s: any) => s.id === activeVar.sim_id) || data.sim_variants[0])
      } else {
        if (data?.colors?.length > 0) setSelectedColorObj(data.colors[0])
        if (data?.memory_variants?.length > 0) setSelectedStorageObj(data.memory_variants[0])
        if (data?.sim_variants?.length > 0) setSelectedSimObj(data.sim_variants[0])
      }
    }

    ApiService.getProductBySlug(productId)
      .then((data) => {
        if (data && (data.id || data.slug)) {
          initSelection(data)
        } else {
          ApiService.getProducts({ page_size: 100 })
            .then((res: any) => {
              const list = res.results || res || []
              const found = list.find((p: any) => p.id === productId || p.slug === productId) || list[0]
              if (found) initSelection(found)
            })
            .catch(() => {})
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [productId])

  const colorHexMap: Record<string, string> = {
    'Серебристый': '#E2E4E1',
    'Silver': '#E2E4E1',
    'Космический серый': '#4B494E',
    'Space Gray': '#4B494E',
    'Золотой': '#F5E7D3',
    'Gold': '#F5E7D3',
    'Черный': '#1C1D21',
    'Black': '#1C1D21',
    'Темно-синий': '#202A36',
    'Midnight': '#202A36',
    'Оранжевый': '#E86D2A',
    'Синий': '#0055A5',
    'Белый': '#F8F9FA'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-slate-600 font-bold text-sm">Загрузка карточки товара...</p>
        </div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <h1 className="text-xl font-bold text-slate-800">Товар не найден</h1>
        <Link href="/catalog" className="mt-4 px-6 py-2 bg-emerald-600 text-white font-bold rounded-xl text-sm">
          Вернуться в каталог
        </Link>
      </div>
    )
  }

  const variants: any[] = product.variants || []

  const matchedVariant = variants.find(
    (v) =>
      (!selectedColorObj || String(v.color_id) === String(selectedColorObj.id)) &&
      (!selectedStorageObj || String(v.memory_id) === String(selectedStorageObj.id)) &&
      (!selectedSimObj || String(v.sim_id) === String(selectedSimObj.id))
  )

  const isColorAvailableForSelectedCombination = (colorId: string) => {
    if (variants.length === 0) return true
    return variants.some(
      (v) =>
        String(v.color_id) === String(colorId) &&
        (!selectedStorageObj || String(v.memory_id) === String(selectedStorageObj.id)) &&
        (!selectedSimObj || String(v.sim_id) === String(selectedSimObj.id)) &&
        v.is_active &&
        v.stock > 0
    )
  }

  const baseRaw = Number(product.discount_price || product.base_price || product.price || 0)
  let calculatedPrice = baseRaw
  let oldPriceDisplay: number | null = product.discount_price ? Number(product.base_price) : null
  let currentStock = product.stock

  if (matchedVariant) {
    calculatedPrice = Number(matchedVariant.price)
    oldPriceDisplay = matchedVariant.old_price ? Number(matchedVariant.old_price) : null
    currentStock = matchedVariant.stock
  } else if (selectedStorageObj?.price_override) {
    calculatedPrice = Number(selectedStorageObj.price_override)
    currentStock = selectedStorageObj.stock || currentStock
  } else if (selectedSimObj?.price_override) {
    calculatedPrice = Number(selectedSimObj.price_override)
    currentStock = selectedSimObj.stock || currentStock
  } else if (selectedColorObj?.price_override) {
    calculatedPrice = Number(selectedColorObj.price_override)
    currentStock = selectedColorObj.stock || currentStock
  }

  const formattedPrice = new Intl.NumberFormat('ru-RU').format(calculatedPrice)
  const formattedOldPrice = oldPriceDisplay ? new Intl.NumberFormat('ru-RU').format(oldPriceDisplay) : null
  const brandName = typeof product.brand === 'object' ? product.brand?.name : product.brand || 'BAHO'
  
  const productName = (lang === 'uz' && product.name_uz) ? product.name_uz : (lang === 'en' && product.name_en) ? product.name_en : product.name
  const productDescription = (lang === 'uz' && product.description_uz) ? product.description_uz : (lang === 'en' && product.description_en) ? product.description_en : product.description

  const getColorName = (c: any) => {
    if (!c) return ''
    if (lang === 'uz' && c.name_uz) return c.name_uz
    if (lang === 'en' && c.name_en) return c.name_en
    return c.name
  }

  const getMemoryCapacity = (m: any) => {
    if (!m) return ''
    if (lang === 'uz' && m.capacity_uz) return m.capacity_uz
    if (lang === 'en' && m.capacity_en) return m.capacity_en
    return m.capacity
  }

  const getSimDisplay = (s: any) => {
    if (!s) return ''
    if (s.name_override) return s.name_override
    if (s.sim_type_display) return s.sim_type_display
    return s.sim_type || ''
  }
  
  const allImages = product.images || []
  const colorImages = selectedColorObj
    ? allImages.filter((img: any) => img.color_id && String(img.color_id) === String(selectedColorObj.id))
    : []
  
  let galleryImages = colorImages.length > 0 ? colorImages : (allImages.length > 0 ? [...allImages] : [])
  if (selectedColorObj?.image && !galleryImages.some((i: any) => i.image === selectedColorObj.image)) {
    galleryImages = [{ id: 'color-direct', image: selectedColorObj.image }, ...galleryImages]
  }

  const activeMainImage = galleryImages[activeImageIndex]?.image ||
    selectedColorObj?.image ||
    allImages[0]?.image ||
    product.image ||
    'https://images.unsplash.com/photo-1592286927505-1def25115558?w=500'

  const isSimAvailableForSelectedMemory = (simId: string) => {
    if (variants.length === 0) return true
    return variants.some(
      (v) => (!selectedStorageObj || String(v.memory_id) === String(selectedStorageObj.id)) && String(v.sim_id) === String(simId) && v.is_active && v.stock > 0
    )
  }

  const monthlyPaymentRaw = Math.round(calculatedPrice / selectedMonths)
  const monthlyPaymentFormatted = new Intl.NumberFormat('ru-RU').format(monthlyPaymentRaw)

  const handleAddToCart = async () => {
    setIsAdded(true)
    setTimeout(() => setIsAdded(false), 2000)
    try {
      await ApiService.addToCart(
        product.id,
        quantity,
        matchedVariant?.id,
        selectedColorObj?.id,
        selectedStorageObj?.id
      )
    } catch (e) {
      console.error('Cart error:', e)
    }
  }

  const handleToggleWishlist = async () => {
    setIsWishlisted((prev) => !prev)
    try {
      await ApiService.toggleFavorite(product.id)
    } catch (e) {
      console.error('Wishlist error:', e)
    }
  }

  const handleSubmitQuickOrder = (e: React.FormEvent) => {
    e.preventDefault()
    setOrderSuccess(true)
    setTimeout(() => {
      setOrderSuccess(false)
      setOrderModalOpen(false)
    }, 2500)
  }

  return (
    <>
      <Header />
      <main className="min-h-screen bg-slate-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-6">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-500">
            <Link href="/" className="hover:text-emerald-700 transition">{t('breadcrumbHome')}</Link>
            <span>/</span>
            <Link href="/catalog" className="hover:text-emerald-700 transition">{t('breadcrumbCatalog')}</Link>
            <span>/</span>
            <span className="text-slate-900 font-bold line-clamp-1">{productName}</span>
          </div>
        </div>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="lg:col-span-6 bg-white rounded-3xl border border-slate-200/80 p-6 md:p-8 shadow-sm flex flex-col items-center justify-center relative overflow-hidden sticky top-24"
            >
              <span className="absolute top-4 left-4 z-10 inline-flex items-center gap-1.5 bg-emerald-950 text-emerald-300 text-xs font-extrabold px-3.5 py-1.5 rounded-full shadow-md">
                <Zap className="w-4 h-4 fill-emerald-400 text-emerald-400" /> {t('installmentBadge')}
              </span>

              <div className="w-full aspect-square max-h-[420px] flex items-center justify-center p-4">
                <img
                  src={activeMainImage}
                  alt={productName}
                  className="w-full h-full object-contain drop-shadow-2xl transition-all duration-300 hover:scale-105"
                />
              </div>

              {galleryImages.length > 1 && (
                <div className="flex items-center justify-center gap-3 mt-4 pt-4 border-t border-slate-100 w-full overflow-x-auto pb-1 scrollbar-none">
                  {galleryImages.map((imgObj: any, index: number) => {
                    const isCurrent = activeImageIndex === index
                    return (
                      <button
                        key={imgObj.id || index}
                        onClick={() => setActiveImageIndex(index)}
                        className={`w-14 h-14 rounded-2xl p-1.5 border-2 transition-all flex items-center justify-center bg-slate-50 flex-shrink-0 ${
                          isCurrent
                            ? 'border-emerald-600 shadow-md scale-105 bg-white'
                            : 'border-slate-200 opacity-70 hover:opacity-100 hover:border-slate-300'
                        }`}
                      >
                        <img
                          src={imgObj.image}
                          alt={`Thumbnail ${index + 1}`}
                          className="w-full h-full object-contain"
                        />
                      </button>
                    )
                  })}
                </div>
              )}
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="lg:col-span-6 space-y-6"
            >
              <div className="bg-white rounded-3xl border border-slate-200/80 p-6 md:p-8 shadow-sm space-y-6">
                <div>
                  <span className="text-xs font-black text-emerald-700 uppercase tracking-widest block mb-1">
                    {brandName}
                  </span>
                  <h1 className="text-2xl sm:text-3xl font-black text-slate-900 leading-tight">
                    {productName}
                  </h1>
                  {matchedVariant?.sku && (
                    <span className="text-xs font-bold text-slate-400 tracking-wide mt-1 block">
                      SKU: {matchedVariant.sku}
                    </span>
                  )}
                </div>

                <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative overflow-hidden">
                  <div className="absolute right-0 top-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-2xl pointer-events-none" />
                  <div>
                    <span className="text-xs text-slate-400 font-semibold block mb-1">{t('cashPrice')}</span>
                    <div className="flex items-baseline gap-2">
                      <span className="text-3xl font-black text-white">
                        {formattedPrice} <span className="text-sm font-semibold text-slate-400">{t('sum')}</span>
                      </span>
                      {formattedOldPrice && (
                        <span className="text-sm text-slate-400 line-through font-bold">
                          {formattedOldPrice} {t('sum')}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="sm:text-right border-t sm:border-t-0 sm:border-l border-slate-800 pt-3 sm:pt-0 sm:pl-6">
                    <span className="text-xs text-emerald-400 font-extrabold block">{t('inInstallmentFor')}</span>
                    <span className="text-xl font-black text-emerald-400">
                      {monthlyPaymentFormatted} <span className="text-xs text-white">{t('sum')}/{t('monthSuffix')}</span>
                    </span>
                  </div>
                </div>

                {product.memory_variants?.length > 0 && (
                  <div className="space-y-3">
                    <label className="text-xs font-extrabold text-slate-700 uppercase tracking-wider block">
                      {t('memoryXotira')}
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {product.memory_variants.map((mem: any, idx: number) => {
                        const isSelected = selectedStorageObj?.id === mem.id
                        const defaultCapacities = ['256GB', '512GB', '1TB', '2TB']
                        const capVal = getMemoryCapacity(mem)
                        const displayCapacity = (capVal && capVal !== 'Память') 
                          ? capVal 
                          : defaultCapacities[idx] || '256GB'

                        return (
                          <button
                            key={mem.id}
                            onClick={() => setSelectedStorageObj(mem)}
                            className={`px-4 py-2.5 rounded-xl font-extrabold text-xs transition border ${
                              isSelected
                                ? 'bg-slate-900 text-white border-slate-900 shadow-md'
                                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                            }`}
                          >
                            {displayCapacity}
                          </button>
                        )
                      })}
                    </div>
                  </div>
                )}

                {product.sim_variants?.length > 0 && (
                  <div className="space-y-3">
                    <label className="text-xs font-extrabold text-slate-700 uppercase tracking-wider block">
                      {t('simConfig')}
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {product.sim_variants.map((sim: any) => {
                        const isSelected = selectedSimObj?.id === sim.id
                        const isAvailable = isSimAvailableForSelectedMemory(sim.id)
                        return (
                          <button
                            key={sim.id}
                            disabled={!isAvailable}
                            onClick={() => setSelectedSimObj(sim)}
                            className={`px-4 py-2.5 rounded-xl font-extrabold text-xs transition border ${
                              isSelected
                                ? 'bg-slate-900 text-white border-slate-900 shadow-md'
                                : isAvailable
                                ? 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                                : 'bg-slate-100 text-slate-400 border-slate-200 line-through opacity-50 cursor-not-allowed'
                            }`}
                          >
                            {getSimDisplay(sim)}
                          </button>
                        )
                      })}
                    </div>
                  </div>
                )}

                {product.colors?.length > 0 && (
                  <div className="space-y-3">
                    <label className="text-xs font-extrabold text-slate-700 uppercase tracking-wider block">
                      {t('colorRang')} <span className="text-emerald-700 ml-1 font-bold">{getColorName(selectedColorObj)}</span>
                    </label>
                    <div className="flex items-center gap-3">
                      {product.colors.map((color: any) => {
                        const isSelected = selectedColorObj?.id === color.id
                        const isAvailable = isColorAvailableForSelectedCombination(color.id)
                        const cName = getColorName(color)
                        return (
                          <button
                            key={color.id}
                            disabled={!isAvailable}
                            onClick={() => {
                              setSelectedColorObj(color)
                              setActiveImageIndex(0)
                            }}
                            className={`w-10 h-10 rounded-full p-0.5 transition-all flex items-center justify-center relative ${
                              isSelected
                                ? 'ring-2 ring-emerald-600 ring-offset-2 scale-110'
                                : isAvailable
                                ? 'hover:scale-105 opacity-80 hover:opacity-100'
                                : 'opacity-30 cursor-not-allowed'
                            }`}
                            title={cName}
                          >
                            <span
                              className="w-full h-full rounded-full border border-slate-300 shadow-inner"
                              style={{ backgroundColor: color.hex_code || '#2B2B2B' }}
                            />
                            {!isAvailable && (
                              <span className="absolute inset-0 flex items-center justify-center text-slate-600 font-bold text-xs">
                                ✕
                              </span>
                            )}
                          </button>
                        )
                      })}
                    </div>
                  </div>
                )}

                <div className="bg-emerald-50/70 border border-emerald-200/80 p-5 rounded-2xl space-y-3">
                  <div className="flex items-center gap-2 text-emerald-900 font-extrabold text-xs tracking-wide uppercase">
                    <Calculator className="w-4 h-4 text-emerald-700" />
                    <span>{t('selectTerm')}</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2">
                    {installmentMonths.map((item) => (
                      <button
                        key={item.months}
                        onClick={() => setSelectedMonths(item.months)}
                        className={`py-2.5 rounded-xl font-black text-xs transition flex flex-col items-center justify-center ${
                          selectedMonths === item.months
                            ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30 scale-105'
                            : 'bg-white text-slate-800 hover:bg-emerald-100/50 border border-emerald-200'
                        }`}
                      >
                        <span>{item.months} {t('monthSuffix')}</span>
                      </button>
                    ))}
                  </div>
                  <div className="text-[11px] font-bold text-emerald-900 text-center pt-1">
                    {t('monthlyPaymentShort')} <span className="text-sm font-black text-emerald-700">{monthlyPaymentFormatted} {t('sum')}/{t('monthSuffix')}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between py-2 border-y border-slate-100">
                  <span className="text-xs font-extrabold text-slate-700 uppercase tracking-wider">{t('quantity')}</span>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      className="w-9 h-9 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl font-bold transition flex items-center justify-center text-base"
                    >
                      −
                    </button>
                    <span className="text-base font-black text-slate-900 w-6 text-center">{quantity}</span>
                    <button
                      onClick={() => setQuantity(quantity + 1)}
                      className="w-9 h-9 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl font-bold transition flex items-center justify-center text-base"
                    >
                      +
                    </button>
                  </div>
                </div>

                <div className="space-y-3 pt-2">
                  <div className="flex items-center gap-3">
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handleAddToCart}
                      className={`flex-1 py-4 text-white font-extrabold text-sm rounded-2xl transition-all shadow-md flex items-center justify-center gap-2 ${
                        isAdded ? 'bg-emerald-600' : 'bg-emerald-700 hover:bg-emerald-800 shadow-emerald-700/20'
                      }`}
                    >
                      {isAdded ? (
                        <>
                          <Check className="w-5 h-5" /> Добавлено!
                        </>
                      ) : (
                        <>
                          <ShoppingCart className="w-5 h-5" /> {t('addToCart')}
                        </>
                      )}
                    </motion.button>

                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleToggleWishlist}
                      className={`p-4 rounded-2xl border transition-all shadow-sm ${
                        isWishlisted
                          ? 'bg-rose-50 border-rose-200 text-rose-500'
                          : 'bg-white border-slate-200 hover:border-rose-400 text-slate-400 hover:text-rose-500'
                      }`}
                    >
                      <Heart className="w-5 h-5" fill={isWishlisted ? 'currentColor' : 'none'} />
                    </motion.button>
                  </div>

                  <button
                    onClick={() => setOrderModalOpen(true)}
                    className="w-full py-3.5 bg-slate-900 hover:bg-slate-800 text-white font-extrabold text-xs uppercase tracking-wider rounded-2xl transition flex items-center justify-center gap-2 shadow-lg"
                  >
                    <Sparkles className="w-4 h-4 text-emerald-400" />
                    {t('quickOrder')}
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4 border-t border-slate-100 text-xs text-slate-600 font-medium">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                    <span>{t('officialWarrantyShort')}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Truck className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                    <span>{t('deliveryInHours')}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <RefreshCw className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                    <span>{t('tradeInExchange')}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          <div className="mt-12 bg-white rounded-3xl border border-slate-200/80 p-8 shadow-sm space-y-6">
            <h2 className="text-2xl font-black text-slate-900">{t('descAndSpecs')}</h2>
            <div className="prose max-w-none text-slate-600 text-sm leading-relaxed space-y-4">
              <p>
                {productDescription ||
                  `Оригинальный ${productName} с официальной гарантией 12 месяцев.`}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-slate-100">
              <div className="flex justify-between py-2 border-b border-slate-100 text-xs">
                <span className="text-slate-500 font-bold">{t('manufacturer')}</span>
                <span className="font-extrabold text-slate-900">{brandName}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-slate-100 text-xs">
                <span className="text-slate-500 font-bold">{t('selectedColorLabel')}</span>
                <span className="font-extrabold text-slate-900">{getColorName(selectedColorObj) || '—'}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-slate-100 text-xs">
                <span className="text-slate-500 font-bold">{t('memoryCapacityLabel')}</span>
                <span className="font-extrabold text-slate-900">{getMemoryCapacity(selectedStorageObj) || '—'}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-slate-100 text-xs">
                <span className="text-slate-500 font-bold">{t('warrantyLabel')}</span>
                <span className="font-extrabold text-emerald-700">{t('yearOfficial')}</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {orderModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-sm flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl relative"
          >
            <button
              onClick={() => setOrderModalOpen(false)}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 flex items-center justify-center font-bold text-xs"
            >
              ✕
            </button>

            {orderSuccess ? (
              <div className="text-center py-6 space-y-3">
                <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
                  <Check className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-black text-slate-900">Заявка отправлена!</h3>
                <p className="text-xs text-slate-500">
                  Менеджер BAHO MARKET свяжется с вами в течение 5 минут для подтверждения рассрочки.
                </p>
              </div>
            ) : (
              <form onSubmit={handleSubmitQuickOrder} className="space-y-4">
                <div className="flex items-center gap-2 text-emerald-800 font-black text-lg mb-1">
                  <PhoneCall className="w-5 h-5 text-emerald-600" />
                  <span>Быстрая рассрочка</span>
                </div>
                <p className="text-xs text-slate-500">
                  Оставьте ваш номер телефона для быстрого оформления рассрочки на {productName} ({selectedMonths} мес).
                </p>

                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-bold text-slate-700 block mb-1">Ваше имя</label>
                    <input
                      type="text"
                      required
                      placeholder="Имя"
                      value={customerName}
                      onChange={(e) => setCustomerName(e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs font-bold focus:outline-none focus:border-emerald-600"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-bold text-slate-700 block mb-1">Номер телефона</label>
                    <input
                      type="tel"
                      required
                      placeholder="+998 77 371-08-08"
                      value={customerPhone}
                      onChange={(e) => setCustomerPhone(e.target.value)}
                      className="w-full px-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs font-bold focus:outline-none focus:border-emerald-600"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-xs uppercase tracking-wider rounded-xl transition shadow-md shadow-emerald-600/20 mt-2"
                >
                  Отправить заявку
                </button>
              </form>
            )}
          </motion.div>
        </div>
      )}

      <Footer />
    </>
  )
}
