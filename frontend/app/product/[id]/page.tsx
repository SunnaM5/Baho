import { ProductPageClient } from './product-client'

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  return <ProductPageClient productId={id} />
}

export async function generateStaticParams() {
  return [
    { id: 'e130c1d6-f6ef-4af1-870d-b9b99120acc6' }
  ]
}
