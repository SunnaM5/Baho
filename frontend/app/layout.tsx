import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import './globals.css'
import { LanguageProvider } from '@/context/language-context'

export const metadata: Metadata = {
  title: 'BAHO MARKET - Premium Electronics Store',
  description: 'Premium electronics store. Smartphones, laptops, tablets, and accessories with installment plans.',
  generator: 'v0.app',
  keywords: 'smartphones, electronics, Apple, Samsung, Xiaomi, laptops, tablets, naushniki, accessories',
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1.0,
  maximumScale: 1.0,
  userScalable: false,
  colorScheme: 'light dark',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#0B5D3B' },
    { media: '(prefers-color-scheme: dark)', color: '#11B981' },
  ],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="bg-background overflow-x-hidden" suppressHydrationWarning>
      <body className="antialiased font-sans w-full max-w-full overflow-x-hidden" suppressHydrationWarning>
        <LanguageProvider>
          {children}
        </LanguageProvider>
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
