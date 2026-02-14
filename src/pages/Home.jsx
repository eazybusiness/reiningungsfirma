import { motion } from 'framer-motion'
import { CheckCircle, Clock, Shield, Star, Sparkles, Building2, Home as HomeIcon, Droplets } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Home() {
  const services = [
    {
      icon: Building2,
      title: 'Büroreinigung',
      description: 'Professionelle Reinigung für Büros, Praxen und Geschäftsräume',
      image: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&auto=format&fit=crop'
    },
    {
      icon: HomeIcon,
      title: 'Privatreinigung',
      description: 'Zuverlässige Haushaltsreinigung für Ihr Zuhause',
      image: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=800&auto=format&fit=crop'
    },
    {
      icon: Droplets,
      title: 'Fensterreinigung',
      description: 'Streifenfreie Fenster für klare Durchsicht',
      image: 'https://images.unsplash.com/photo-1628177142898-93e36e4e3a50?w=800&auto=format&fit=crop'
    },
    {
      icon: Sparkles,
      title: 'Grundreinigung',
      description: 'Intensive Reinigung für besondere Anlässe',
      image: 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&auto=format&fit=crop'
    }
  ]

  const features = [
    { icon: CheckCircle, title: 'Zertifizierte Fachkräfte', description: 'Geschultes und erfahrenes Personal' },
    { icon: Clock, title: 'Flexible Zeiten', description: 'Reinigung nach Ihrem Zeitplan' },
    { icon: Shield, title: 'Versichert & Bonded', description: 'Vollständig versichert für Ihre Sicherheit' },
    { icon: Star, title: '100% Zufriedenheit', description: 'Garantierte Qualität oder Geld zurück' }
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 to-blue-800 text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-3xl"
          >
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
              Professionelle Reinigung für Ihr Unternehmen
            </h1>
            <p className="text-xl sm:text-2xl mb-8 text-blue-100">
              Zuverlässig, gründlich und termingerecht – Ihre Reinigungsfirma in Berlin
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                to="/kontakt"
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition-colors text-center"
              >
                Kostenloses Angebot anfordern
              </Link>
              <Link
                to="/leistungen"
                className="bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-800 transition-colors text-center border-2 border-white/20"
              >
                Unsere Leistungen
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                  <feature.icon className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2 text-gray-900">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Unsere Leistungen
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Von der Büroreinigung bis zur Grundreinigung – wir bieten maßgeschneiderte Lösungen für jeden Bedarf
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {services.map((service, index) => (
              <motion.div
                key={service.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow"
              >
                <div className="h-48 overflow-hidden">
                  <img
                    src={service.image}
                    alt={service.title}
                    className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <div className="p-6">
                  <div className="flex items-center mb-3">
                    <div className="bg-blue-100 p-2 rounded-lg mr-3">
                      <service.icon className="h-6 w-6 text-blue-600" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900">{service.title}</h3>
                  </div>
                  <p className="text-gray-600 mb-4">{service.description}</p>
                  <Link
                    to="/leistungen"
                    className="text-blue-600 font-medium hover:text-blue-700 inline-flex items-center"
                  >
                    Mehr erfahren
                    <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              Bereit für eine saubere Zukunft?
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Kontaktieren Sie uns noch heute für ein kostenloses, unverbindliches Angebot
            </p>
            <Link
              to="/kontakt"
              className="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              Jetzt Angebot anfordern
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
