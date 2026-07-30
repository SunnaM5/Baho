'use client'

import { Header } from '@/components/header'
import { Hero } from '@/components/hero'
import { Categories } from '@/components/categories'
import { DealsOfDay } from '@/components/deals-of-day'
import { PopularProducts } from '@/components/popular-products'
import { Installments } from '@/components/installments'
import { Brands } from '@/components/brands'
import { WhyUs } from '@/components/why-us'
import { TradeIn } from '@/components/trade-in'
import { Footer } from '@/components/footer'

export default function Page() {
  return (
    <>
      <Header />
      <main className="min-h-screen">
        {/* Hero Section */}
        <section className="px-3 sm:px-6 lg:px-8 py-3 sm:py-8 lg:py-12 max-w-7xl mx-auto w-full">
          <Hero />
        </section>

        {/* Categories Carousel */}
        <section className="px-3 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
          <Categories />
        </section>

        {/* Deals of the Day */}
        <section className="px-3 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
          <DealsOfDay />
        </section>

        {/* Popular Products / Electronics Catalog */}
        <section className="px-3 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
          <PopularProducts />
        </section>

        {/* Installments Calculator */}
        <section className="px-3 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
          <Installments />
        </section>

        {/* Brands Ticker */}
        <section className="px-3 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
          <Brands />
        </section>

        {/* Why Choose Us */}
        <section className="px-3 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
          <WhyUs />
        </section>

        {/* Trade-In */}
        <section className="px-3 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
          <TradeIn />
        </section>
      </main>
      <Footer />
    </>
  )
}
