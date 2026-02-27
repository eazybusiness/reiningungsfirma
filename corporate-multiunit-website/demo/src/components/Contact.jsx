import { motion } from 'framer-motion'
import { useInView } from './useInView'
import { Mail, Phone, MapPin, ArrowRight } from 'lucide-react'

export default function Contact() {
  const [ref, isInView] = useInView(0.15)

  return (
    <section id="contact" ref={ref} className="py-28 lg:py-36 bg-navy-950">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5 }}
            className="flex items-center justify-center gap-4 mb-6"
          >
            <div className="w-16 h-[2px] bg-gold-400" />
            <span className="text-gold-400 text-xs font-semibold tracking-[0.35em] uppercase">
              Kontakt
            </span>
            <div className="w-16 h-[2px] bg-gold-400" />
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="font-serif text-3xl md:text-4xl lg:text-5xl text-white mb-5 leading-tight"
          >
            Lassen Sie uns <span className="text-gold-400">ins Gespräch kommen.</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-white/50 text-lg max-w-xl mx-auto"
          >
            Ob strategische Partnerschaft oder konkretes Projekt — wir freuen uns
            auf Ihre Anfrage und melden uns zeitnah bei Ihnen.
          </motion.p>
        </div>

        <div className="grid lg:grid-cols-5 gap-12 lg:gap-16">
          {/* Left — Contact info */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={isInView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="lg:col-span-2 space-y-8"
          >
            <ContactInfo icon={Mail} label="E-Mail" value="info@apex-industries.de" />
            <ContactInfo icon={Phone} label="Telefon" value="+49 (0) 123 456 789" />
            <ContactInfo icon={MapPin} label="Standort" value="Musterstraße 10, 60313 Frankfurt am Main" />

            {/* Decorative element */}
            <div className="pt-8 hidden lg:block">
              <div className="w-24 h-[1px] bg-gradient-to-r from-gold-400/30 to-transparent" />
              <p className="text-white/30 text-xs mt-4 leading-relaxed max-w-[200px]">
                Wir melden uns innerhalb von 24 Stunden bei Ihnen.
              </p>
            </div>
          </motion.div>

          {/* Right — Form */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.35 }}
            className="lg:col-span-3 bg-navy-900 border border-navy-800 p-8 md:p-10"
          >
            <h3 className="text-white font-semibold text-lg mb-8 flex items-center gap-3">
              <div className="w-8 h-[2px] bg-gold-400" />
              Anfrage senden
            </h3>

            <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
              <div className="grid sm:grid-cols-2 gap-5">
                <div>
                  <label className="text-white/40 text-xs font-medium tracking-wide uppercase mb-2.5 block">Name *</label>
                  <input
                    type="text"
                    placeholder="Max Mustermann"
                    className="w-full bg-navy-950 border border-navy-700 text-white px-4 py-3.5 text-sm placeholder:text-white/20 transition-colors"
                  />
                </div>
                <div>
                  <label className="text-white/40 text-xs font-medium tracking-wide uppercase mb-2.5 block">Unternehmen</label>
                  <input
                    type="text"
                    placeholder="Firma GmbH"
                    className="w-full bg-navy-950 border border-navy-700 text-white px-4 py-3.5 text-sm placeholder:text-white/20 transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="text-white/40 text-xs font-medium tracking-wide uppercase mb-2.5 block">E-Mail *</label>
                <input
                  type="email"
                  placeholder="max@firma.de"
                  className="w-full bg-navy-950 border border-navy-700 text-white px-4 py-3.5 text-sm placeholder:text-white/20 transition-colors"
                />
              </div>

              <div>
                <label className="text-white/40 text-xs font-medium tracking-wide uppercase mb-2.5 block">Betreff</label>
                <select
                  className="w-full bg-navy-950 border border-navy-700 text-white px-4 py-3.5 text-sm transition-colors"
                  defaultValue=""
                >
                  <option value="" disabled>Bitte wählen...</option>
                  <option>Allgemeine Anfrage</option>
                  <option>Partnerschaft</option>
                  <option>Industrial Manufacturing</option>
                  <option>Engineering Services</option>
                  <option>Logistics & Supply Chain</option>
                  <option>Digital Solutions</option>
                  <option>Sustainable Energy</option>
                </select>
              </div>

              <div>
                <label className="text-white/40 text-xs font-medium tracking-wide uppercase mb-2.5 block">Nachricht *</label>
                <textarea
                  rows={5}
                  placeholder="Ihre Nachricht..."
                  className="w-full bg-navy-950 border border-navy-700 text-white px-4 py-3.5 text-sm placeholder:text-white/20 transition-colors resize-none"
                />
              </div>

              <button
                type="submit"
                className="w-full flex items-center justify-center gap-2 bg-gold-400 text-navy-950 font-bold text-sm tracking-[0.15em] uppercase px-6 py-4 hover:bg-gold-300 transition-all duration-300"
              >
                Nachricht senden
                <ArrowRight size={16} />
              </button>
            </form>
          </motion.div>
        </div>
      </div>

      {/* Bottom gold divider */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-gold-400/20 to-transparent" />
    </section>
  )
}

function ContactInfo({ icon: Icon, label, value }) {
  return (
    <div className="flex items-start gap-4 group">
      <div className="flex-shrink-0 w-12 h-12 bg-navy-900 border border-navy-800 flex items-center justify-center group-hover:border-gold-400/40 transition-colors duration-300">
        <Icon className="text-gold-400" size={18} />
      </div>
      <div>
        <p className="text-white/35 text-[11px] font-medium tracking-[0.2em] uppercase mb-1">{label}</p>
        <p className="text-white/80 text-sm font-medium">{value}</p>
      </div>
    </div>
  )
}
