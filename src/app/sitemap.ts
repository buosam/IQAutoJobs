import { MetadataRoute } from 'next'
 
export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://iqautojobs.com'
  
  // Static routes
  const staticRoutes = [
    '',
    '/jobs',
    '/companies',
    '/auth/login',
    '/auth/register',
  ].map(route => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 1,
  }))
  
  // Dynamic routes would be fetched from your database
  // For now, we'll add some placeholder dynamic routes
  const dynamicRoutes = [
    {
      url: `${baseUrl}/jobs/1`,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/companies/1`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    },
  ]
  
  return [...staticRoutes, ...dynamicRoutes]
}