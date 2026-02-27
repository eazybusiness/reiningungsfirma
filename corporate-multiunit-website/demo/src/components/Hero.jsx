import { motion } from 'framer-motion'
import { ChevronDown, ArrowRight } from 'lucide-react'

export default function Hero() {
  return (
    <section id="hero" className="relative min-h-screen flex items-end bg-navy-950 overflow-hidden">
      {/* Background image */}
      <div className="absolute inset-0">
        <img
          src="./hero.jpg"
          alt=""
          className="w-full h-full object-cover object-top"
        />
        {/* Reason: Multi-layer overlay for readability + brand color integration */}
        <div className="absolute inset-0 bg-navy-950/60" />
        <div className="absolute inset-0 bg-gradient-to-t from-navy-950 via-navy-950/40 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-r from-navy-950/80 via-transparent to-transparent" />
      </div>

      {/* Content */}
      <div className="relative w-full max-w-7xl mx-auto px-6 lg:px-8 pb-24 pt-40">
        <div className="max-w-3xl">
          {/* Overline */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
            className="flex items-center gap-4 mb-8"
          >
            <div className="w-16 h-[2px] bg-gold-400" />
            <span className="text-gold-400 text-xs sm:text-sm font-semibold tracking-[0.35em] uppercase">
              Industrielle Unternehmensgruppe
            </span>
          </motion.div>

          {/* Heading */}
          <motion.h1
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.15 }}
            className="font-serif text-5xl sm:text-6xl md:text-7xl lg:text-8xl text-white leading-[1.05] mb-8"
          >
            Kompetenz.
            <br />
            <span className="text-gold-400">Struktur.</span>
            <br />
            Vertrauen.
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.35 }}
            className="text-white/70 text-lg md:text-xl leading-relaxed mb-12 max-w-xl"
          >
            Fünf spezialisierte Divisionen. Eine gemeinsame Vision.
            Als integrierte Business Group vereinen wir industrielle Exzellenz
            mit strategischer Weitsicht.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.55 }}
            className="flex flex-col sm:flex-row gap-4"
          >
            <a
              href="#divisions"
              className="group inline-flex items-center justify-center gap-2 px-8 py-4 bg-gold-400 text-navy-950 font-bold text-sm tracking-[0.15em] uppercase hover:bg-gold-300 transition-all duration-300"
            >
              Unsere Divisionen
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </a>
            <a
              href="#about"
              className="inline-flex items-center justify-center px-8 py-4 border border-white/25 text-white font-medium text-sm tracking-[0.15em] uppercase hover:border-gold-400 hover:text-gold-400 transition-all duration-300 backdrop-blur-sm"
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
        transition={{ delay: 1.5 }}
        className="absolute bottom-6 left-1/2 -translate-x-1/2"
      >
        <motion.a
          href="#about"
          animate={{ y: [0, 10, 0] }}
          transition={{ repeat: Infinity, duration: 2.5 }}
          className="block"
        >
          <ChevronDown className="text-gold-400/50" size={32} />
        </motion.a>
      </motion.div>

      {/* Bottom gold divider */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-gold-400/30 to-transparent" />
    </section>
  )
}
