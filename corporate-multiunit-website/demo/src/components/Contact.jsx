import { motion } from 'framer-motion'
import { useInView } from './useInView'
import { Mail, Phone, MapPin, ArrowRight } from 'lucide-react'

export default function Contact() {
  const [ref, isInView] = useInView(0.2)

  return (
    <section id="contact" ref={ref} className="py-24 lg:py-32 bg-white">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 lg:gap-24">
          {/* Left — Info */}
          <div>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={isInView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.6 }}
              className="flex items-center gap-4 mb-6"
            >
              <div className="w-12 h-px bg-gold-400" />
              <span className="text-gold-500 text-sm font-medium tracking-[0.3em] uppercase">
                Kontakt
              </span>
            </motion.div>

            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="font-serif text-3xl md:text-4xl lg:text-5xl text-navy-900 mb-6 leading-tight"
            >
              Lassen Sie uns
              <br />
              <span className="text-gold-500">ins Gespräch kommen.</span>
            </motion.h2>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-navy-500 leading-relaxed mb-10"
            >
              Ob strategische Partnerschaft oder konkretes Projekt — wir freuen uns
              auf Ihre Anfrage und melden uns zeitnah bei Ihnen.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="space-y-6"
            >
              <ContactInfo icon={Mail} label="E-Mail" value="info@apex-industries.de" />
              <ContactInfo icon={Phone} label="Telefon" value="+49 (0) 123 456 789" />
              <ContactInfo icon={MapPin} label="Standort" value="Musterstraße 10, 60313 Frankfurt am Main" />
            </motion.div>
          </div>

          {/* Right — Form */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="bg-navy-900 p-8 md:p-10"
          >
            <h3 className="text-white font-semibold text-xl mb-6">Anfrage senden</h3>

            <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
              <div className="grid sm:grid-cols-2 gap-5">
                <div>
                  <label className="text-navy-300 text-sm mb-2 block">Name *</label>
                  <input
                    type="text"
                    placeholder="Max Mustermann"
                    className="w-full bg-navy-800 border border-navy-700 text-white px-4 py-3 text-sm placeholder:text-navy-500 focus:outline-none focus:border-gold-400 transition-colors"
                  />
                </div>
                <div>
                  <label className="text-navy-300 text-sm mb-2 block">Unternehmen</label>
                  <input
                    type="text"
                    placeholder="Firma GmbH"
                    className="w-full bg-navy-800 border border-navy-700 text-white px-4 py-3 text-sm placeholder:text-navy-500 focus:outline-none focus:border-gold-400 transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="text-navy-300 text-sm mb-2 block">E-Mail *</label>
                <input
                  type="email"
                  placeholder="max@firma.de"
                  className="w-full bg-navy-800 border border-navy-700 text-white px-4 py-3 text-sm placeholder:text-navy-500 focus:outline-none focus:border-gold-400 transition-colors"
                />
              </div>

              <div>
                <label className="text-navy-300 text-sm mb-2 block">Betreff</label>
                <select
                  className="w-full bg-navy-800 border border-navy-700 text-white px-4 py-3 text-sm focus:outline-none focus:border-gold-400 transition-colors"
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
                <label className="text-navy-300 text-sm mb-2 block">Nachricht *</label>
                <textarea
                  rows={4}
                  placeholder="Ihre Nachricht..."
                  className="w-full bg-navy-800 border border-navy-700 text-white px-4 py-3 text-sm placeholder:text-navy-500 focus:outline-none focus:border-gold-400 transition-colors resize-none"
                />
              </div>

              <button
                type="submit"
                className="w-full flex items-center justify-center gap-2 bg-gold-400 text-navy-900 font-semibold text-sm tracking-wide uppercase px-6 py-4 hover:bg-gold-300 transition-colors duration-300"
              >
                Nachricht senden
                <ArrowRight size={16} />
              </button>
            </form>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

function ContactInfo({ icon: Icon, label, value }) {
  return (
    <div className="flex items-start gap-4">
      <div className="w-10 h-10 bg-navy-50 border border-navy-100 flex items-center justify-center flex-shrink-0">
        <Icon className="text-gold-500" size={18} />
      </div>
      <div>
        <p className="text-navy-400 text-xs font-medium tracking-wide uppercase mb-0.5">{label}</p>
        <p className="text-navy-800 text-sm font-medium">{value}</p>
      </div>
    </div>
  )
}
