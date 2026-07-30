const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export async function fetchAPI(endpoint: string, options: RequestInit = {}, isRetry: boolean = false) {
  const defaultHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    'Accept-Language': typeof window !== 'undefined' ? localStorage.getItem('lang') || 'ru' : 'ru',
  };

  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    
    // If token is invalid or expired, clear it and retry public endpoints without token
    if (res.status === 401 && token && !isRetry) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
      return fetchAPI(endpoint, options, true);
    }

    throw new Error(errorData.detail || errorData.message || `API error: ${res.status}`);
  }

  return res.json();
}

// API Services
export const ApiService = {
  // CMS & Home
  getHomeCMS: () => fetchAPI('/api/v1/cms/home/'),

  // Products & Catalog
  getProducts: (params: string = '') => fetchAPI(`/api/v1/products/?${params}`),
  getProductBySlug: (slug: string) => fetchAPI(`/api/v1/products/${slug}/`),

  // Categories & Brands
  getCategories: () => fetchAPI('/api/v1/categories/'),
  getBrands: () => fetchAPI('/api/v1/brands/'),

  // Search
  search: (query: string) => fetchAPI(`/api/v1/search/?q=${encodeURIComponent(query)}`),

  // Cart
  getCart: () => fetchAPI('/api/v1/cart/'),
  addToCart: (productId: string, quantity: number = 1, variantId?: string, colorId?: string, memoryVariantId?: string) =>
    fetchAPI('/api/v1/cart/items/', {
      method: 'POST',
      body: JSON.stringify({
        product_id: productId,
        quantity,
        variant_id: variantId,
        color_id: colorId,
        memory_variant_id: memoryVariantId
      }),
    }),

  // Favorites
  getFavorites: () => fetchAPI('/api/v1/favorites/'),
  toggleFavorite: (productId: string) =>
    fetchAPI('/api/v1/favorites/toggle/', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId }),
    }),

  // SEO
  getSeoMeta: (entityType: string = 'home', slug?: string) =>
    fetchAPI(`/api/v1/seo/meta/?entity_type=${entityType}${slug ? `&slug=${slug}` : ''}`),
};
