import { motion } from 'framer-motion'
import { useInView } from './useInView'
import { Mail, Phone, MapPin, Send } from 'lucide-react'

export default function Contact() {
  const [ref, isInView] = useInView(0.1)

  return (
    <section id="contact" ref={ref} className="bg-navy-950 py-32 lg:py-44">
      <div className="max-w-[1200px] mx-auto px-6 lg:px-10">

        <div className="grid lg:grid-cols-2 gap-20 lg:gap-28">
          {/* Left — Invitation text + contact details */}
          <div>
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5 }}
              className="text-gold-400 text-[12px] font-semibold tracking-[0.2em] uppercase mb-6"
            >
              Kontakt
            </motion.p>

            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.7, delay: 0.05 }}
              className="font-serif text-[clamp(1.8rem,4vw,3rem)] text-white leading-[1.25] mb-8"
            >
              Lassen Sie uns gemeinsam die nächsten Schritte planen.
            </motion.h2>

            <motion.p
              initial={{ opacity: 0, y: 15 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.15 }}
              className="text-white/45 text-[15px] leading-[1.8] mb-14 max-w-md"
            >
              Ob strategische Partnerschaft, Projektanfrage oder ein erstes
              Kennenlernen — wir freuen uns auf Ihre Nachricht.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.25 }}
              className="space-y-7"
            >
              <ContactLine icon={Mail} value="info@apex-industries.de" />
              <ContactLine icon={Phone} value="+49 (0) 123 456 789" />
              <ContactLine icon={MapPin} value="Musterstraße 10, 60313 Frankfurt am Main" />
            </motion.div>
          </div>

          {/* Right — Modern form */}
          <motion.div
            initial={{ opacity: 0, y: 25 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.7, delay: 0.2 }}
          >
            <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
              <div className="grid sm:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Ihr Name *"
                  className="w-full bg-white/[0.06] border border-white/[0.08] text-white px-5 py-4 text-[14px] rounded-xl placeholder:text-white/25 focus:border-gold-400/40 focus:bg-white/[0.08] transition-all duration-300"
                />
                <input
                  type="text"
                  placeholder="Unternehmen"
                  className="w-full bg-white/[0.06] border border-white/[0.08] text-white px-5 py-4 text-[14px] rounded-xl placeholder:text-white/25 focus:border-gold-400/40 focus:bg-white/[0.08] transition-all duration-300"
                />
              </div>

              <input
                type="email"
                placeholder="E-Mail Adresse *"
                className="w-full bg-white/[0.06] border border-white/[0.08] text-white px-5 py-4 text-[14px] rounded-xl placeholder:text-white/25 focus:border-gold-400/40 focus:bg-white/[0.08] transition-all duration-300"
              />

              <select
                className="w-full bg-white/[0.06] border border-white/[0.08] text-white/25 px-5 py-4 text-[14px] rounded-xl focus:border-gold-400/40 focus:bg-white/[0.08] transition-all duration-300 appearance-none"
                defaultValue=""
              >
                <option value="" disabled>Betreff wählen...</option>
                <option className="bg-navy-900 text-white">Allgemeine Anfrage</option>
                <option className="bg-navy-900 text-white">Partnerschaft</option>
                <option className="bg-navy-900 text-white">Industrial Manufacturing</option>
                <option className="bg-navy-900 text-white">Engineering Services</option>
                <option className="bg-navy-900 text-white">Logistics & Supply Chain</option>
                <option className="bg-navy-900 text-white">Digital Solutions</option>
                <option className="bg-navy-900 text-white">Sustainable Energy</option>
              </select>

              <textarea
                rows={5}
                placeholder="Ihre Nachricht..."
                className="w-full bg-white/[0.06] border border-white/[0.08] text-white px-5 py-4 text-[14px] rounded-xl placeholder:text-white/25 focus:border-gold-400/40 focus:bg-white/[0.08] transition-all duration-300 resize-none"
              />

              <button
                type="submit"
                className="w-full sm:w-auto flex items-center justify-center gap-3 bg-gold-400 text-navy-950 text-[13px] font-semibold tracking-[0.06em] px-8 py-4 rounded-full hover:bg-gold-300 transition-colors duration-300"
              >
                Nachricht senden
                <Send size={14} />
              </button>

              <p className="text-white/20 text-[12px] pt-2">
                Wir melden uns in der Regel innerhalb von 24 Stunden.
              </p>
            </form>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

function ContactLine({ icon: Icon, value }) {
  return (
    <div className="flex items-center gap-4">
      <Icon className="text-gold-400/60 flex-shrink-0" size={18} />
      <span className="text-white/60 text-[14px]">{value}</span>
    </div>
  )
}
