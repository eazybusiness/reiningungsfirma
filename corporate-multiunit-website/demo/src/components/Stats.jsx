import { motion } from 'framer-motion'
import { useInView } from './useInView'

const stats = [
  { value: '25+', label: 'Jahre Erfahrung' },
  { value: '5', label: 'Divisionen' },
  { value: '800+', label: 'Mitarbeiter' },
  { value: '12', label: 'Standorte' },
]

export default function Stats() {
  const [ref, isInView] = useInView(0.3)

  return (
    <section ref={ref} className="py-20 bg-navy-900 relative overflow-hidden">
      {/* Subtle gold line top */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-gold-400/40 to-transparent" />

      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="text-center"
            >
              <div className="text-gold-400 font-serif text-4xl md:text-5xl font-bold mb-2">
                {stat.value}
              </div>
              <div className="text-navy-300 text-sm tracking-wide uppercase">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Subtle gold line bottom */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-gold-400/40 to-transparent" />
    </section>
  )
}
