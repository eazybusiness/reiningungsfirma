import { motion } from 'framer-motion'
import { useInView } from './useInView'

export default function Mission() {
  const [ref, isInView] = useInView(0.2)

  return (
    <section ref={ref} className="bg-navy-950 py-32 lg:py-40">
      <div className="max-w-[1200px] mx-auto px-6 lg:px-10">
        <div className="max-w-3xl mx-auto text-center">

          {/* Reason: A chairman quote signals trust and governance — what banks/investors look for */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.7 }}
          >
            <div className="w-12 h-[2px] bg-gold-400 mx-auto mb-10" />

            <blockquote className="font-serif text-[clamp(1.3rem,3vw,2rem)] text-white/90 leading-[1.5] mb-10">
              &bdquo;Nachhaltiges Wachstum entsteht nicht durch Geschwindigkeit,
              sondern durch Substanz. Unsere Aufgabe ist es, Strukturen zu schaffen,
              die Generationen überdauern.&ldquo;
            </blockquote>

            <div className="flex items-center justify-center gap-4">
              <div className="w-10 h-10 rounded-full bg-navy-800 flex items-center justify-center">
                <span className="text-gold-400 font-serif text-sm font-semibold">MH</span>
              </div>
              <div className="text-left">
                <p className="text-white text-sm font-medium">Dr. Michael Hartmann</p>
                <p className="text-white/40 text-[12px]">Vorsitzender der Geschäftsführung</p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
