import { MetadataRoute } from 'next'
 
export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://iqautojobs.com'
  
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/admin/', '/employer/', '/candidate/', '/api/'],
    },
    sitemap: `${baseUrl}/sitemap.xml`,
  }
}