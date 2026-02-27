import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X } from 'lucide-react'

const navLinks = [
  { label: 'Über uns', href: '#about' },
  { label: 'Divisionen', href: '#divisions' },
  { label: 'Kontakt', href: '#contact' },
]

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-navy-950 border-b border-white/[0.06]">
      <div className="max-w-[1200px] mx-auto px-6 lg:px-10">
        <div className="flex items-center justify-between h-[72px]">
          {/* Logo */}
          <a href="#hero" className="flex items-center gap-3">
            <img
              src="./logo.png"
              alt="APEX Industries Group"
              className="h-9 w-auto"
            />
            <div className="hidden sm:block leading-none">
              <span className="text-white font-semibold text-[15px] tracking-wider block">
                APEX
              </span>
              <span className="text-white/40 text-[9px] block tracking-[0.25em] uppercase mt-0.5">
                Industries Group
              </span>
            </div>
          </a>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-12">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-white/60 hover:text-white text-[13px] font-normal tracking-[0.08em] transition-colors duration-300"
              >
                {link.label}
              </a>
            ))}
            <a
              href="#contact"
              className="ml-4 px-6 py-2 bg-gold-400 text-navy-950 text-[12px] font-semibold tracking-[0.1em] uppercase rounded-full hover:bg-gold-300 transition-colors duration-300"
            >
              Kontakt aufnehmen
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden text-white/60 p-2 hover:text-white transition-colors"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Menü"
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.25 }}
            className="lg:hidden bg-navy-950 border-t border-white/[0.06] overflow-hidden"
          >
            <div className="px-6 py-8 space-y-6">
              {navLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className="block text-white/60 hover:text-white text-sm transition-colors"
                >
                  {link.label}
                </a>
              ))}
              <a
                href="#contact"
                onClick={() => setMobileOpen(false)}
                className="block mt-4 px-6 py-3 bg-gold-400 text-navy-950 text-sm font-semibold tracking-wide text-center rounded-full hover:bg-gold-300 transition-colors"
              >
                Kontakt aufnehmen
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}
