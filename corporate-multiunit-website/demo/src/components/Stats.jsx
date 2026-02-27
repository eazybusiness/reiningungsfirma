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
    <section ref={ref} className="py-20 lg:py-24 bg-navy-950 relative overflow-hidden">
      {/* Top gold divider */}
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-gold-400/30 to-transparent" />

      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-10 lg:gap-16">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5, delay: index * 0.12 }}
              className="text-center relative"
            >
              <div className="text-gold-400 font-serif text-5xl md:text-6xl font-bold mb-3">
                {stat.value}
              </div>
              <div className="text-white/40 text-xs tracking-[0.2em] uppercase font-medium">
                {stat.label}
              </div>
              {/* Reason: Vertical separator between stats, hidden on last item */}
              {index < stats.length - 1 && (
                <div className="hidden lg:block absolute right-0 top-1/2 -translate-y-1/2 w-[1px] h-12 bg-gradient-to-b from-transparent via-gold-400/20 to-transparent -mr-8" />
              )}
            </motion.div>
          ))}
        </div>
      </div>

      {/* Bottom gold divider */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-gold-400/30 to-transparent" />
    </section>
  )
}
