import { motion } from 'framer-motion'
import { useInView } from './useInView'
import { Factory, Wrench, Truck, Cpu, Leaf, ArrowUpRight } from 'lucide-react'

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
  const [ref, isInView] = useInView(0.05)

  return (
    <section id="divisions" ref={ref} className="py-28 lg:py-36 bg-navy-900">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-20">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5 }}
            className="flex items-center justify-center gap-4 mb-6"
          >
            <div className="w-16 h-[2px] bg-gold-400" />
            <span className="text-gold-400 text-xs font-semibold tracking-[0.35em] uppercase">
              Unsere Divisionen
            </span>
            <div className="w-16 h-[2px] bg-gold-400" />
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="font-serif text-3xl md:text-4xl lg:text-5xl text-white mb-5"
          >
            Fünf Säulen. <span className="text-gold-400">Ein Standard.</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-white/50 text-lg max-w-2xl mx-auto"
          >
            Jede Division operiert eigenständig — und doch profitieren alle von den
            Synergien einer starken Gruppe.
          </motion.p>
        </div>

        {/* Division cards — top row of 3, bottom row of 2 centered */}
        <div className="space-y-6">
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

      {/* Bottom gold divider */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-gold-400/20 to-transparent" />
    </section>
  )
}

function DivisionCard({ division, index, isInView }) {
  const Icon = division.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.5, delay: 0.15 + index * 0.08 }}
      className="group bg-navy-800/50 border border-navy-700/50 p-8 hover:border-gold-400/30 hover:bg-navy-800 transition-all duration-500 h-full relative overflow-hidden"
    >
      {/* Hover glow effect */}
      <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-gold-400 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

      {/* Icon + arrow */}
      <div className="flex items-start justify-between mb-6">
        <div className="w-14 h-14 bg-navy-900 border border-navy-700 flex items-center justify-center group-hover:border-gold-400/40 transition-all duration-500">
          <Icon className="text-gold-400" size={24} />
        </div>
        <ArrowUpRight className="text-white/0 group-hover:text-gold-400 transition-all duration-500 mt-1" size={20} />
      </div>

      {/* Title */}
      <h3 className="text-white font-semibold text-lg mb-1 group-hover:text-gold-400 transition-colors duration-300">{division.name}</h3>
      <p className="text-gold-400/70 text-sm font-medium mb-4">{division.subtitle}</p>

      {/* Description */}
      <p className="text-white/45 text-sm leading-relaxed mb-6">{division.description}</p>

      {/* Tags */}
      <div className="flex flex-wrap gap-2">
        {division.tags.map((tag) => (
          <span
            key={tag}
            className="text-[11px] bg-navy-900/80 text-white/50 px-3 py-1 font-medium tracking-wide border border-navy-700/50"
          >
            {tag}
          </span>
        ))}
      </div>
    </motion.div>
  )
}
