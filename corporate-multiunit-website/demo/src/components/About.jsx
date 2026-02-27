import { motion } from 'framer-motion'
import { useInView } from './useInView'

export default function About() {
  const [ref, isInView] = useInView(0.1)

  return (
    <section id="about" ref={ref} className="bg-white py-32 lg:py-44">
      <div className="max-w-[1200px] mx-auto px-6 lg:px-10">

        {/* Section label */}
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5 }}
          className="text-gold-600 text-[12px] font-semibold tracking-[0.2em] uppercase mb-6"
        >
          Unternehmensprofil
        </motion.p>

        {/* Reason: Large editorial heading — this is how Siemens/Danaher do it */}
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7, delay: 0.05 }}
          className="font-serif text-[clamp(1.8rem,4vw,3.2rem)] text-navy-900 leading-[1.25] max-w-3xl mb-16 lg:mb-20"
        >
          Die APEX Industries Group vereint fünf spezialisierte Divisionen unter
          einem gemeinsamen Qualitätsversprechen — seit über 25 Jahren.
        </motion.h2>

        {/* Two-column body text — editorial feel */}
        <div className="grid md:grid-cols-2 gap-12 lg:gap-20">
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.15 }}
          >
            <p className="text-navy-700 text-[15px] leading-[1.8] mb-6">
              Als industrielle Unternehmensgruppe mit Sitz in Deutschland decken
              unsere Divisionen das gesamte Spektrum moderner Industriedienstleistungen
              ab — von der Fertigung über Engineering bis hin zu Logistik und digitaler
              Transformation.
            </p>
            <p className="text-navy-500 text-[15px] leading-[1.8]">
              Unsere Struktur ermöglicht es, die Agilität spezialisierter Einheiten
              mit der Leistungsfähigkeit einer integrierten Gruppe zu verbinden.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.25 }}
          >
            <p className="text-navy-700 text-[15px] leading-[1.8] mb-6">
              Was uns verbindet: gebündelte Ressourcen, gemeinsame Qualitätsstandards
              und die Überzeugung, dass nachhaltige Partnerschaften der Schlüssel zu
              wirtschaftlichem Erfolg sind.
            </p>
            <p className="text-navy-500 text-[15px] leading-[1.8]">
              Für unsere Partner bedeutet das: ein Ansprechpartner, viele Kompetenzen.
              Für unser Team: ein klarer Rahmen, in dem Exzellenz gedeiht.
            </p>
          </motion.div>
        </div>

        {/* Key figures — subtle, not a Baukasten counter */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, delay: 0.35 }}
          className="mt-20 lg:mt-28 pt-12 border-t border-navy-100"
        >
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 lg:gap-16">
            {[
              { value: '25+', label: 'Jahre' },
              { value: '5', label: 'Divisionen' },
              { value: '800+', label: 'Mitarbeitende' },
              { value: '12', label: 'Standorte' },
            ].map((item) => (
              <div key={item.label}>
                <div className="text-navy-900 font-serif text-3xl md:text-4xl font-semibold mb-1">
                  {item.value}
                </div>
                <div className="text-navy-400 text-[13px]">
                  {item.label}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
