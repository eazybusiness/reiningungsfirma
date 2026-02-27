import { motion } from 'framer-motion'
import { useInView } from './useInView'
import { Factory, Wrench, Truck, Cpu, Leaf } from 'lucide-react'

const divisions = [
  {
    icon: Factory,
    name: 'Industrial Manufacturing',
    subtitle: 'Fertigung & Produktion',
    description:
      'Hochpräzise Fertigungsprozesse für industrielle Komponenten. Von der Prototypenentwicklung bis zur Serienproduktion.',
    tags: ['CNC-Bearbeitung', 'Qualitätssicherung', 'Serienfertigung'],
  },
  {
    icon: Wrench,
    name: 'Engineering Services',
    subtitle: 'Ingenieursdienstleistungen',
    description:
      'Technische Beratung und Engineering-Lösungen für komplexe industrielle Herausforderungen.',
    tags: ['Planung', 'Konstruktion', 'Projektmanagement'],
  },
  {
    icon: Truck,
    name: 'Logistics & Supply Chain',
    subtitle: 'Logistik & Lieferkette',
    description:
      'Effiziente Supply-Chain-Lösungen, die Ihre Produktions- und Distributionsketten optimieren.',
    tags: ['Warehousing', 'Distribution', 'Fulfillment'],
  },
  {
    icon: Cpu,
    name: 'Digital Solutions',
    subtitle: 'Digitale Transformation',
    description:
      'Industrie 4.0 und digitale Prozessoptimierung. Wir verbinden Tradition mit Innovation.',
    tags: ['IoT', 'Automation', 'Datenanalyse'],
  },
  {
    icon: Leaf,
    name: 'Sustainable Energy',
    subtitle: 'Nachhaltige Energie',
    description:
      'Energieeffiziente Lösungen und nachhaltige Technologien für eine zukunftsfähige Industrie.',
    tags: ['Energieberatung', 'Nachhaltigkeit', 'Zertifizierung'],
  },
]

export default function Divisions() {
  const [ref, isInView] = useInView(0.1)

  return (
    <section id="divisions" ref={ref} className="py-24 lg:py-32 bg-gray-50">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5 }}
            className="flex items-center justify-center gap-4 mb-6"
          >
            <div className="w-12 h-px bg-gold-400" />
            <span className="text-gold-500 text-sm font-medium tracking-[0.3em] uppercase">
              Unsere Divisionen
            </span>
            <div className="w-12 h-px bg-gold-400" />
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="font-serif text-3xl md:text-4xl lg:text-5xl text-navy-900 mb-4"
          >
            Fünf Säulen. <span className="text-gold-500">Ein Standard.</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-navy-500 text-lg max-w-2xl mx-auto"
          >
            Jede Division operiert eigenständig — und doch profitieren alle von den
            Synergien einer starken Gruppe.
          </motion.p>
        </div>

        {/* Division cards — top row of 3, bottom row of 2 centered */}
        <div className="space-y-6">
          {/* Top row */}
          <div className="grid md:grid-cols-3 gap-6">
            {divisions.slice(0, 3).map((division, index) => (
              <DivisionCard
                key={division.name}
                division={division}
                index={index}
                isInView={isInView}
              />
            ))}
          </div>
          {/* Bottom row — centered */}
          <div className="flex flex-col md:flex-row gap-6 justify-center">
            {divisions.slice(3, 5).map((division, index) => (
              <div key={division.name} className="md:w-[calc(33.333%-0.5rem)]">
                <DivisionCard
                  division={division}
                  index={index + 3}
                  isInView={isInView}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

function DivisionCard({ division, index, isInView }) {
  const Icon = division.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
      className="group bg-white border border-gray-200 p-8 hover:border-gold-400/50 hover:shadow-lg transition-all duration-500 h-full"
    >
      {/* Icon */}
      <div className="w-14 h-14 bg-navy-900 flex items-center justify-center mb-6 group-hover:bg-gold-400 transition-colors duration-500">
        <Icon className="text-gold-400 group-hover:text-navy-900 transition-colors duration-500" size={24} />
      </div>

      {/* Title */}
      <h3 className="text-navy-900 font-semibold text-xl mb-1">{division.name}</h3>
      <p className="text-gold-500 text-sm font-medium mb-4">{division.subtitle}</p>

      {/* Description */}
      <p className="text-navy-500 text-sm leading-relaxed mb-6">{division.description}</p>

      {/* Tags */}
      <div className="flex flex-wrap gap-2">
        {division.tags.map((tag) => (
          <span
            key={tag}
            className="text-xs bg-navy-50 text-navy-600 px-3 py-1 font-medium"
          >
            {tag}
          </span>
        ))}
      </div>

      {/* Bottom accent line */}
      <div className="mt-6 w-0 group-hover:w-full h-0.5 bg-gold-400 transition-all duration-500" />
    </motion.div>
  )
}
