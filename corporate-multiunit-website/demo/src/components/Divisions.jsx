import { motion } from 'framer-motion'
import { useInView } from './useInView'
import { ArrowRight } from 'lucide-react'

const divisions = [
  {
    number: '01',
    name: 'Industrial Manufacturing',
    subtitle: 'Fertigung & Produktion',
    description:
      'Hochpräzise Fertigungsprozesse für industrielle Komponenten. Von der Prototypenentwicklung bis zur Serienproduktion.',
  },
  {
    number: '02',
    name: 'Engineering Services',
    subtitle: 'Ingenieursdienstleistungen',
    description:
      'Technische Beratung und Engineering-Lösungen für komplexe industrielle Herausforderungen.',
  },
  {
    number: '03',
    name: 'Logistics & Supply Chain',
    subtitle: 'Logistik & Lieferkette',
    description:
      'Effiziente Supply-Chain-Lösungen, die Ihre Produktions- und Distributionsketten optimieren.',
  },
  {
    number: '04',
    name: 'Digital Solutions',
    subtitle: 'Digitale Transformation',
    description:
      'Industrie 4.0 und digitale Prozessoptimierung. Wir verbinden Tradition mit Innovation.',
  },
  {
    number: '05',
    name: 'Sustainable Energy',
    subtitle: 'Nachhaltige Energie',
    description:
      'Energieeffiziente Lösungen und nachhaltige Technologien für eine zukunftsfähige Industrie.',
  },
]

export default function Divisions() {
  const [ref, isInView] = useInView(0.05)

  return (
    <section id="divisions" ref={ref} className="bg-[#F8F8F6] py-32 lg:py-44">
      <div className="max-w-[1200px] mx-auto px-6 lg:px-10">

        {/* Section header */}
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5 }}
          className="text-gold-600 text-[12px] font-semibold tracking-[0.2em] uppercase mb-6"
        >
          Divisionen
        </motion.p>

        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.05 }}
          className="font-serif text-[clamp(1.8rem,4vw,3.2rem)] text-navy-900 leading-[1.25] max-w-2xl mb-20 lg:mb-28"
        >
          Fünf spezialisierte Einheiten. Ein gemeinsamer Qualitätsanspruch.
        </motion.h2>

        {/* Reason: List layout instead of card grid — feels more editorial, less template */}
        <div className="space-y-0">
          {divisions.map((division, index) => (
            <motion.div
              key={division.number}
              initial={{ opacity: 0, y: 15 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5, delay: 0.1 + index * 0.06 }}
              className="group border-t border-navy-200/60 py-10 md:py-12 grid md:grid-cols-12 gap-6 md:gap-10 items-start cursor-pointer hover:bg-white/60 transition-colors duration-500 -mx-6 md:-mx-10 px-6 md:px-10"
            >
              {/* Number */}
              <div className="md:col-span-1">
                <span className="text-navy-300 text-[13px] font-mono">{division.number}</span>
              </div>

              {/* Name */}
              <div className="md:col-span-4">
                <h3 className="text-navy-900 text-lg md:text-xl font-semibold group-hover:text-gold-600 transition-colors duration-300">
                  {division.name}
                </h3>
                <p className="text-navy-400 text-[13px] mt-1">{division.subtitle}</p>
              </div>

              {/* Description */}
              <div className="md:col-span-5">
                <p className="text-navy-500 text-[14px] leading-[1.7]">
                  {division.description}
                </p>
              </div>

              {/* Arrow */}
              <div className="md:col-span-2 flex md:justify-end">
                <ArrowRight
                  size={18}
                  className="text-navy-300 group-hover:text-gold-500 group-hover:translate-x-1 transition-all duration-300 mt-1"
                />
              </div>
            </motion.div>
          ))}
          {/* Bottom border for last item */}
          <div className="border-t border-navy-200/60" />
        </div>
      </div>
    </section>
  )
}
