import { motion } from 'framer-motion'
import { ArrowDown } from 'lucide-react'

export default function Hero() {
  return (
    <section id="hero" className="relative bg-navy-950 overflow-hidden pt-[72px]">
      {/* Reason: Two-part hero — text on top, image below with overlay blending into navy */}
      <div className="max-w-[1200px] mx-auto px-6 lg:px-10">

        {/* Text content — generous vertical space */}
        <div className="pt-24 md:pt-32 lg:pt-40 pb-16 md:pb-20 lg:pb-24">
          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-gold-400 text-[13px] font-medium tracking-[0.2em] uppercase mb-8"
          >
            Industrielle Unternehmensgruppe
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1 }}
            className="font-serif text-[clamp(2.5rem,6vw,5.5rem)] text-white leading-[1.1] mb-8 max-w-4xl"
          >
            Wir verbinden industrielle Kompetenz mit{' '}
            <span className="text-gold-400">strategischer Weitsicht.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.25 }}
            className="text-white/50 text-lg md:text-xl leading-relaxed max-w-2xl mb-12"
          >
            Fünf spezialisierte Divisionen. Eine gemeinsame Vision. Als integrierte
            Business Group schaffen wir nachhaltigen Mehrwert für Partner, Kunden
            und Gesellschaft.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4"
          >
            <a
              href="#about"
              className="inline-flex items-center justify-center gap-3 px-8 py-3.5 bg-gold-400 text-navy-950 text-[13px] font-semibold tracking-[0.06em] rounded-full hover:bg-gold-300 transition-colors duration-300"
            >
              Unternehmen kennenlernen
            </a>
            <a
              href="#divisions"
              className="inline-flex items-center justify-center gap-3 px-8 py-3.5 text-white/60 text-[13px] font-medium tracking-[0.06em] hover:text-white transition-colors duration-300"
            >
              Unsere Divisionen
              <ArrowDown size={14} className="opacity-40" />
            </a>
          </motion.div>
        </div>
      </div>

      {/* Hero image — centered, with overlay fade to navy */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0.3 }}
        className="relative h-[50vh] md:h-[60vh] lg:h-[70vh] overflow-hidden"
      >
        <img
          src="./hero.jpg"
          alt="APEX Industries Group — Unser Team"
          className="w-full h-full object-cover object-center"
        />
        {/* Reason: Top fade blends image into the text section above */}
        <div className="absolute inset-0 bg-gradient-to-b from-navy-950 via-transparent to-navy-950" />
        <div className="absolute inset-0 bg-navy-950/30" />
      </motion.div>
    </section>
  )
}
