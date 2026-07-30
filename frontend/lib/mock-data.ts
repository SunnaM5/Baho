export interface Product {
  id: string
  name: string
  brand: string
  price: number
  discount?: number
  image: string
  rating: number
  reviews: number
  inStock: boolean
  installments?: {
    months: number
    amount: number
  }[]
  category: string
  specs?: string[]
}

export interface Brand {
  id: string
  name: string
  logo: string
}

export const products: Product[] = [
  {
    id: '1',
    name: 'iPhone 15 Pro Max',
    brand: 'Apple',
    price: 1299000,
    discount: 10,
    image: 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=500&h=500&fit=crop',
    rating: 4.9,
    reviews: 324,
    inStock: true,
    category: 'Smartphones',
    installments: [
      { months: 3, amount: 433000 },
      { months: 6, amount: 216500 },
      { months: 12, amount: 108250 },
    ],
  },
  {
    id: '2',
    name: 'Samsung Galaxy S24 Ultra',
    brand: 'Samsung',
    price: 1199000,
    discount: 8,
    image: 'https://images.unsplash.com/photo-1610945415295-d9bbf7e3b3fe?w=500&h=500&fit=crop',
    rating: 4.8,
    reviews: 456,
    inStock: true,
    category: 'Smartphones',
    installments: [
      { months: 3, amount: 399667 },
      { months: 6, amount: 199833 },
      { months: 12, amount: 99917 },
    ],
  },
  {
    id: '3',
    name: 'Xiaomi 14 Ultra',
    brand: 'Xiaomi',
    price: 899000,
    discount: 15,
    image: 'https://images.unsplash.com/photo-1606933248051-5ce98adc4ecf?w=500&h=500&fit=crop',
    rating: 4.7,
    reviews: 203,
    inStock: true,
    category: 'Smartphones',
    installments: [
      { months: 3, amount: 299667 },
      { months: 6, amount: 149833 },
      { months: 12, amount: 74917 },
    ],
  },
  {
    id: '4',
    name: 'MacBook Pro 14"',
    brand: 'Apple',
    price: 2499000,
    image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&h=500&fit=crop',
    rating: 4.9,
    reviews: 512,
    inStock: true,
    category: 'Laptops',
    installments: [
      { months: 6, amount: 416500 },
      { months: 12, amount: 208250 },
      { months: 24, amount: 104125 },
    ],
  },
  {
    id: '5',
    name: 'Dell XPS 15',
    brand: 'Dell',
    price: 1899000,
    discount: 12,
    image: 'https://images.unsplash.com/photo-1588872657840-218e412ee62e?w=500&h=500&fit=crop',
    rating: 4.6,
    reviews: 267,
    inStock: true,
    category: 'Laptops',
    installments: [
      { months: 6, amount: 316500 },
      { months: 12, amount: 158250 },
      { months: 24, amount: 79125 },
    ],
  },
  {
    id: '6',
    name: 'iPad Air',
    brand: 'Apple',
    price: 799000,
    image: 'https://images.unsplash.com/photo-1585790050230-9f3c91865587?w=500&h=500&fit=crop',
    rating: 4.8,
    reviews: 389,
    inStock: true,
    category: 'Tablets',
    installments: [
      { months: 3, amount: 266333 },
      { months: 6, amount: 133167 },
      { months: 12, amount: 66583 },
    ],
  },
  {
    id: '7',
    name: 'Sony WH-1000XM5',
    brand: 'Sony',
    price: 399000,
    discount: 5,
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop',
    rating: 4.9,
    reviews: 1203,
    inStock: true,
    category: 'Headphones',
    installments: [
      { months: 3, amount: 133000 },
      { months: 6, amount: 66500 },
    ],
  },
  {
    id: '8',
    name: 'Apple Watch Series 9',
    brand: 'Apple',
    price: 429000,
    image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop',
    rating: 4.7,
    reviews: 678,
    inStock: true,
    category: 'Smart Watches',
    installments: [
      { months: 3, amount: 143000 },
      { months: 6, amount: 71500 },
    ],
  },
]

export const brands: Brand[] = [
  { id: '1', name: 'Apple', logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/100px-Apple_logo_black.svg.png' },
  { id: '2', name: 'Samsung', logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Samsung_Logo.svg/100px-Samsung_Logo.svg.png' },
  { id: '3', name: 'Xiaomi', logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Xiaomi_logo.svg/100px-Xiaomi_logo.svg.png' },
  { id: '4', name: 'Honor', logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Honor_logo.svg/100px-Honor_logo.svg.png' },
  { id: '5', name: 'OnePlus', logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/OnePlus_logo.svg/100px-OnePlus_logo.svg.png' },
  { id: '6', name: 'Google Pixel', logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Google_Pixel_phone_logo.svg/100px-Google_Pixel_phone_logo.svg.png' },
]

export const categories = [
  { id: 'smartphones', name: 'Smartphones', icon: 'Smartphone' },
  { id: 'iphone', name: 'iPhones', icon: 'Apple' },
  { id: 'samsung', name: 'Samsung', icon: 'Zap' },
  { id: 'xiaomi', name: 'Xiaomi', icon: 'Radio' },
  { id: 'laptops', name: 'Laptops', icon: 'Laptop' },
  { id: 'tablets', name: 'Tablets', icon: 'Tablet' },
  { id: 'headphones', name: 'Headphones', icon: 'Headphones' },
  { id: 'watches', name: 'Smart Watches', icon: 'Watch' },
]

export const testimonials = [
  {
    id: '1',
    name: 'Akmal Hoshimov',
    rating: 5,
    text: 'Amazing service and fast delivery. Got my iPhone within 2 days!',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
  },
  {
    id: '2',
    name: 'Laylo Shodmonova',
    rating: 5,
    text: 'The installment option made it so easy to get the MacBook I wanted.',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop',
  },
  {
    id: '3',
    name: 'Dilshod Karimov',
    rating: 4,
    text: 'Great prices and original products. Will definitely shop here again.',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop',
  },
]
