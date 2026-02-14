import { motion } from 'framer-motion'
import { Building2, Home, Droplets, Sparkles, Briefcase, Wrench, CheckCircle } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Services() {
  const services = [
    {
      icon: Building2,
      title: 'Büroreinigung',
      description: 'Professionelle Reinigung für Büros, Praxen und Geschäftsräume. Wir sorgen für eine saubere und produktive Arbeitsumgebung.',
      features: [
        'Tägliche oder wöchentliche Reinigung',
        'Schreibtische und Arbeitsflächen',
        'Sanitäranlagen',
        'Küchen und Pausenräume',
        'Böden und Teppiche',
        'Mülltrennung und Entsorgung'
      ],
      image: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&auto=format&fit=crop'
    },
    {
      icon: Home,
      title: 'Privatreinigung',
      description: 'Zuverlässige Haushaltsreinigung für Ihr Zuhause. Mehr Zeit für die wichtigen Dinge im Leben.',
      features: [
        'Regelmäßige Haushaltsreinigung',
        'Bad und WC',
        'Küche inkl. Geräte',
        'Staubsaugen und Wischen',
        'Staubwischen',
        'Flexible Terminvereinbarung'
      ],
      image: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=1200&auto=format&fit=crop'
    },
    {
      icon: Droplets,
      title: 'Fensterreinigung',
      description: 'Streifenfreie Fenster für klare Durchsicht. Innen und außen, auch in schwer zugänglichen Bereichen.',
      features: [
        'Fenster innen und außen',
        'Rahmen und Fensterbänke',
        'Auch Wintergärten',
        'Professionelle Ausrüstung',
        'Streifenfreies Ergebnis',
        'Auch für Gewerbe'
      ],
      image: 'https://images.unsplash.com/photo-1628177142898-93e36e4e3a50?w=1200&auto=format&fit=crop'
    },
    {
      icon: Sparkles,
      title: 'Grundreinigung',
      description: 'Intensive Tiefenreinigung für besondere Anlässe. Ideal bei Umzug, Renovierung oder als Frühjahrsputz.',
      features: [
        'Komplette Tiefenreinigung',
        'Alle Räume gründlich',
        'Auch schwer erreichbare Stellen',
        'Fenster inklusive',
        'Küche und Bad intensiv',
        'Ideal bei Umzug'
      ],
      image: 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=1200&auto=format&fit=crop'
    },
    {
      icon: Briefcase,
      title: 'Praxisreinigung',
      description: 'Hygienische Reinigung für Arztpraxen, Kliniken und medizinische Einrichtungen nach höchsten Standards.',
      features: [
        'Desinfizierende Reinigung',
        'Behandlungsräume',
        'Wartebereiche',
        'Hygiene-Standards',
        'Flexible Zeiten',
        'Zertifiziertes Personal'
      ],
      image: 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=1200&auto=format&fit=crop'
    },
    {
      icon: Wrench,
      title: 'Baureinigung',
      description: 'Professionelle Endreinigung nach Bau- oder Renovierungsarbeiten. Bezugsfertig in kürzester Zeit.',
      features: [
        'Grob- und Feinreinigung',
        'Entfernung von Baustaub',
        'Fenster und Rahmen',
        'Böden grundreinigen',
        'Sanitäranlagen',
        'Schnelle Abwicklung'
      ],
      image: 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=1200&auto=format&fit=crop'
    }
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 to-blue-800 text-white py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-3xl"
          >
            <h1 className="text-4xl sm:text-5xl font-bold mb-6">
              Unsere Leistungen
            </h1>
            <p className="text-xl text-blue-100">
              Maßgeschneiderte Reinigungslösungen für jeden Bedarf – professionell, zuverlässig und termingerecht
            </p>
          </motion.div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="space-y-16">
            {services.map((service, index) => (
              <motion.div
                key={service.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.1 }}
                className={`flex flex-col ${index % 2 === 0 ? 'lg:flex-row' : 'lg:flex-row-reverse'} gap-8 items-center bg-white rounded-2xl overflow-hidden shadow-lg`}
              >
                <div className="lg:w-1/2">
                  <img
                    src={service.image}
                    alt={service.title}
                    className="w-full h-80 object-cover"
                  />
                </div>
                <div className="lg:w-1/2 p-8 lg:p-12">
                  <div className="flex items-center mb-4">
                    <div className="bg-blue-100 p-3 rounded-lg mr-4">
                      <service.icon className="h-8 w-8 text-blue-600" />
                    </div>
                    <h2 className="text-3xl font-bold text-gray-900">{service.title}</h2>
                  </div>
                  <p className="text-lg text-gray-600 mb-6">{service.description}</p>
                  <ul className="space-y-3 mb-6">
                    {service.features.map((feature) => (
                      <li key={feature} className="flex items-start">
                        <CheckCircle className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Link
                    to="/kontakt"
                    className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                  >
                    Angebot anfordern
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
              Nicht das Richtige gefunden?
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Wir bieten auch individuelle Reinigungslösungen an. Kontaktieren Sie uns für ein maßgeschneidertes Angebot.
            </p>
            <Link
              to="/kontakt"
              className="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              Individuelle Anfrage stellen
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
