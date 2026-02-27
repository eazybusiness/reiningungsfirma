import { motion } from 'framer-motion'
import { ChevronDown } from 'lucide-react'

export default function Hero() {
  return (
    <section id="hero" className="relative min-h-screen flex items-center bg-navy-900 overflow-hidden">
      {/* Subtle geometric pattern overlay */}
      <div className="absolute inset-0 opacity-5">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `linear-gradient(45deg, transparent 48%, #C8A960 48%, #C8A960 52%, transparent 52%)`,
            backgroundSize: '60px 60px',
          }}
        />
      </div>

      {/* Gold accent line left */}
      <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-transparent via-gold-400 to-transparent" />

      <div className="relative max-w-7xl mx-auto px-6 lg:px-8 pt-20">
        <div className="max-w-3xl">
          {/* Overline */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="flex items-center gap-4 mb-8"
          >
            <div className="w-12 h-px bg-gold-400" />
            <span className="text-gold-400 text-sm font-medium tracking-[0.3em] uppercase">
              Industrielle Unternehmensgruppe
            </span>
          </motion.div>

          {/* Heading */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="font-serif text-5xl md:text-6xl lg:text-7xl text-white leading-tight mb-6"
          >
            Kompetenz.
            <br />
            <span className="text-gold-400">Struktur.</span>
            <br />
            Vertrauen.
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-navy-200 text-lg md:text-xl leading-relaxed mb-10 max-w-2xl"
          >
            Fünf spezialisierte Divisionen. Eine gemeinsame Vision.
            Als integrierte Business Group vereinen wir industrielle Exzellenz
            mit strategischer Weitsicht.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="flex flex-col sm:flex-row gap-4"
          >
            <a
              href="#divisions"
              className="inline-flex items-center justify-center px-8 py-4 bg-gold-400 text-navy-900 font-semibold text-sm tracking-wide uppercase hover:bg-gold-300 transition-colors duration-300"
            >
              Unsere Divisionen
            </a>
            <a
              href="#about"
              className="inline-flex items-center justify-center px-8 py-4 border border-white/30 text-white font-medium text-sm tracking-wide uppercase hover:border-gold-400 hover:text-gold-400 transition-colors duration-300"
            >
              Über die Gruppe
            </a>
          </motion.div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ repeat: Infinity, duration: 2 }}
        >
          <ChevronDown className="text-gold-400/60" size={28} />
        </motion.div>
      </motion.div>
    </section>
  )
}
