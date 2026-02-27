import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X } from 'lucide-react'

const navLinks = [
  { label: 'Startseite', href: '#hero' },
  { label: 'Über uns', href: '#about' },
  { label: 'Divisionen', href: '#divisions' },
  { label: 'Kontakt', href: '#contact' },
]

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-navy-900/95 backdrop-blur-sm border-b border-gold-400/20">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <a href="#hero" className="flex items-center gap-3">
            <div className="w-10 h-10 border-2 border-gold-400 flex items-center justify-center">
              <span className="text-gold-400 font-serif font-bold text-lg">A</span>
            </div>
            <div>
              <span className="text-white font-semibold text-lg tracking-wide">APEX</span>
              <span className="text-gold-400 text-xs block tracking-[0.25em] uppercase">Industries Group</span>
            </div>
          </a>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-navy-200 hover:text-gold-400 text-sm font-medium tracking-wide uppercase transition-colors duration-300"
              >
                {link.label}
              </a>
            ))}
            <a
              href="#contact"
              className="ml-4 px-6 py-2.5 bg-gold-400 text-navy-900 text-sm font-semibold tracking-wide uppercase hover:bg-gold-300 transition-colors duration-300"
            >
              Anfrage
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-white p-2"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Menü öffnen"
          >
            {mobileOpen ? <X size={24} /> : <Menu size={24} />}
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
            className="md:hidden bg-navy-900 border-t border-gold-400/20"
          >
            <div className="px-6 py-6 space-y-4">
              {navLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className="block text-navy-200 hover:text-gold-400 text-sm font-medium tracking-wide uppercase transition-colors"
                >
                  {link.label}
                </a>
              ))}
              <a
                href="#contact"
                onClick={() => setMobileOpen(false)}
                className="block mt-4 px-6 py-2.5 bg-gold-400 text-navy-900 text-sm font-semibold tracking-wide uppercase text-center hover:bg-gold-300 transition-colors"
              >
                Anfrage
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}
