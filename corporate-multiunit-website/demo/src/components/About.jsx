import { motion } from 'framer-motion'
import { useInView } from './useInView'
import { Shield, Target, Users } from 'lucide-react'

const values = [
  {
    icon: Shield,
    title: 'Verlässlichkeit',
    description: 'Seit über zwei Jahrzehnten ein beständiger Partner für Industrie und Mittelstand.',
  },
  {
    icon: Target,
    title: 'Präzision',
    description: 'Jede Division operiert mit höchster Spezialisierung und klaren Qualitätsstandards.',
  },
  {
    icon: Users,
    title: 'Partnerschaft',
    description: 'Langfristige B2B-Beziehungen auf Augenhöhe — kein Projekt gleicht dem anderen.',
  },
]

export default function About() {
  const [ref, isInView] = useInView(0.2)

  return (
    <section id="about" ref={ref} className="py-24 lg:py-32 bg-white">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 lg:gap-24 items-start">
          {/* Left column — text content */}
          <div>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={isInView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.6 }}
              className="flex items-center gap-4 mb-6"
            >
              <div className="w-12 h-px bg-gold-400" />
              <span className="text-gold-500 text-sm font-medium tracking-[0.3em] uppercase">
                Über uns
              </span>
            </motion.div>

            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="font-serif text-3xl md:text-4xl lg:text-5xl text-navy-900 mb-6 leading-tight"
            >
              Eine Gruppe.
              <br />
              <span className="text-gold-500">Fünf Kompetenzen.</span>
            </motion.h2>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="space-y-4 text-navy-600 leading-relaxed"
            >
              <p>
                Die APEX Industries Group ist eine industrielle Unternehmensgruppe mit Sitz
                in Deutschland. Unsere fünf spezialisierten Divisionen decken das gesamte
                Spektrum moderner Industriedienstleistungen ab.
              </p>
              <p>
                Was uns verbindet: ein gemeinsames Qualitätsversprechen, gebündelte Ressourcen
                und die Überzeugung, dass nachhaltige Partnerschaften der Schlüssel zu
                wirtschaftlichem Erfolg sind.
              </p>
            </motion.div>
          </div>

          {/* Right column — values */}
          <div className="space-y-8">
            {values.map((value, index) => (
              <motion.div
                key={value.title}
                initial={{ opacity: 0, y: 20 }}
                animate={isInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.5, delay: 0.3 + index * 0.15 }}
                className="flex gap-5"
              >
                <div className="flex-shrink-0 w-12 h-12 bg-navy-50 border border-navy-100 flex items-center justify-center">
                  <value.icon className="text-gold-500" size={22} />
                </div>
                <div>
                  <h3 className="text-navy-900 font-semibold text-lg mb-1">{value.title}</h3>
                  <p className="text-navy-500 text-sm leading-relaxed">{value.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
