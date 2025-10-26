"use client"

interface JobPostingSchemaProps {
  title: string
  description: string
  datePosted: string
  validThrough?: string
  employmentType: string
  hiringOrganization: {
    name: string
    sameAs?: string
    logo?: string
  }
  jobLocation: {
    streetAddress?: string
    addressLocality: string
    addressRegion: string
    postalCode?: string
    addressCountry: string
  }
  baseSalary?: {
    currency: string
    value: number
    minValue?: number
    maxValue?: number
    unitText: string
  }
  experienceRequirements?: string
  educationRequirements?: string
  skills?: string[]
  responsibilities?: string[]
  qualifications?: string[]
}

export function JobPostingSchema({
  title,
  description,
  datePosted,
  validThrough,
  employmentType,
  hiringOrganization,
  jobLocation,
  baseSalary,
  experienceRequirements,
  educationRequirements,
  skills,
  responsibilities,
  qualifications,
}: JobPostingSchemaProps) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "JobPosting",
    title,
    description,
    datePosted,
    validThrough,
    employmentType,
    hiringOrganization: {
      "@type": "Organization",
      name: hiringOrganization.name,
      sameAs: hiringOrganization.sameAs,
      logo: hiringOrganization.logo,
    },
    jobLocation: {
      "@type": "Place",
      address: {
        "@type": "PostalAddress",
        streetAddress: jobLocation.streetAddress,
        addressLocality: jobLocation.addressLocality,
        addressRegion: jobLocation.addressRegion,
        postalCode: jobLocation.postalCode,
        addressCountry: jobLocation.addressCountry,
      },
    },
    ...(baseSalary && {
      baseSalary: {
        "@type": "MonetaryAmount",
        currency: baseSalary.currency,
        value: baseSalary.value,
        minValue: baseSalary.minValue,
        maxValue: baseSalary.maxValue,
        unitText: baseSalary.unitText,
      },
    }),
    ...(experienceRequirements && {
      experienceRequirements: {
        "@type": "Text",
        value: experienceRequirements,
      },
    }),
    ...(educationRequirements && {
      educationRequirements: {
        "@type": "Text",
        value: educationRequirements,
      },
    }),
    ...(skills && {
      skills: skills.map(skill => ({
        "@type": "DefinedTerm",
        name: skill,
      })),
    }),
    ...(responsibilities && {
      responsibilities: {
        "@type": "Text",
        value: responsibilities.join("\n"),
      },
    }),
    ...(qualifications && {
      jobBenefits: qualifications.join(", "),
    }),
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  )
}

interface OrganizationSchemaProps {
  name: string
  url?: string
  logo?: string
  description?: string
  address?: {
    streetAddress?: string
    addressLocality: string
    addressRegion: string
    postalCode?: string
    addressCountry: string
  }
  contactPoint?: {
    contactType: string
    telephone?: string
    contactOption?: string
  }
  sameAs?: string[]
}

export function OrganizationSchema({
  name,
  url,
  logo,
  description,
  address,
  contactPoint,
  sameAs,
}: OrganizationSchemaProps) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name,
    url,
    logo,
    description,
    ...(address && {
      address: {
        "@type": "PostalAddress",
        streetAddress: address.streetAddress,
        addressLocality: address.addressLocality,
        addressRegion: address.addressRegion,
        postalCode: address.postalCode,
        addressCountry: address.addressCountry,
      },
    }),
    ...(contactPoint && {
      contactPoint: {
        "@type": "ContactPoint",
        contactType: contactPoint.contactType,
        telephone: contactPoint.telephone,
        contactOption: contactPoint.contactOption,
      },
    }),
    ...(sameAs && {
      sameAs,
    }),
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  )
}

interface WebsiteSchemaProps {
  name: string
  url: string
  description?: string
  searchAction?: string
  potentialAction?: {
    "@type": string
    target: string
    "query-input": string
  }[]
}

export function WebsiteSchema({
  name,
  url,
  description,
  searchAction,
  potentialAction,
}: WebsiteSchemaProps) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name,
    url,
    description,
    ...(searchAction && {
      potentialAction: [
        {
          "@type": "SearchAction",
          target: searchAction,
          "query-input": "required name=search_term_string",
        },
        ...(potentialAction || []),
      ],
    }),
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  )
}

interface BreadcrumbSchemaProps {
  items: {
    name: string
    url: string
  }[]
}

export function BreadcrumbSchema({ items }: BreadcrumbSchemaProps) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  )
}

interface LocalBusinessSchemaProps {
  name: string
  url?: string
  telephone?: string
  address: {
    streetAddress?: string
    addressLocality: string
    addressRegion: string
    postalCode?: string
    addressCountry: string
  }
  geo?: {
    latitude: number
    longitude: number
  }
  openingHours?: string[]
  priceRange?: string
}

export function LocalBusinessSchema({
  name,
  url,
  telephone,
  address,
  geo,
  openingHours,
  priceRange,
}: LocalBusinessSchemaProps) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    name,
    url,
    telephone,
    address: {
      "@type": "PostalAddress",
      streetAddress: address.streetAddress,
      addressLocality: address.addressLocality,
      addressRegion: address.addressRegion,
      postalCode: address.postalCode,
      addressCountry: address.addressCountry,
    },
    ...(geo && {
      geo: {
        "@type": "GeoCoordinates",
        latitude: geo.latitude,
        longitude: geo.longitude,
      },
    }),
    ...(openingHours && {
      openingHoursSpecification: openingHours.map(hours => ({
        "@type": "OpeningHoursSpecification",
        dayOfWeek: hours.split(" ")[0],
        opens: hours.split(" ")[1],
        closes: hours.split(" ")[2],
      })),
    }),
    priceRange,
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  )
}