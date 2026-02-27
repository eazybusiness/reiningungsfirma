import { useState, useEffect } from 'react'
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
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled
          ? 'bg-navy-950/98 backdrop-blur-md shadow-lg shadow-black/20'
          : 'bg-transparent'
      }`}
    >
      {/* Top gold accent line */}
      <div className="h-[2px] bg-gradient-to-r from-gold-600 via-gold-400 to-gold-600" />

      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <a href="#hero" className="flex items-center gap-3 group">
            <img
              src="./logo.png"
              alt="APEX Industries Group"
              className="h-10 w-auto"
            />
            <div className="hidden sm:block">
              <span className="text-white font-semibold text-lg tracking-wider block leading-tight group-hover:text-gold-400 transition-colors duration-300">
                APEX
              </span>
              <span className="text-gold-400 text-[10px] block tracking-[0.3em] uppercase leading-tight">
                Industries Group
              </span>
            </div>
          </a>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-10">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="relative text-white/80 hover:text-gold-400 text-[13px] font-medium tracking-[0.15em] uppercase transition-colors duration-300 py-2 after:absolute after:bottom-0 after:left-0 after:w-0 after:h-[1px] after:bg-gold-400 hover:after:w-full after:transition-all after:duration-300"
              >
                {link.label}
              </a>
            ))}
            <a
              href="#contact"
              className="ml-2 px-7 py-2.5 border border-gold-400 text-gold-400 text-[13px] font-semibold tracking-[0.15em] uppercase hover:bg-gold-400 hover:text-navy-950 transition-all duration-300"
            >
              Anfrage
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden text-white p-2 hover:text-gold-400 transition-colors"
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
            transition={{ duration: 0.3 }}
            className="lg:hidden bg-navy-950/98 backdrop-blur-md border-t border-gold-400/10 overflow-hidden"
          >
            <div className="px-6 py-8 space-y-5">
              {navLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className="block text-white/80 hover:text-gold-400 text-sm font-medium tracking-[0.15em] uppercase transition-colors"
                >
                  {link.label}
                </a>
              ))}
              <a
                href="#contact"
                onClick={() => setMobileOpen(false)}
                className="block mt-6 px-6 py-3 border border-gold-400 text-gold-400 text-sm font-semibold tracking-[0.15em] uppercase text-center hover:bg-gold-400 hover:text-navy-950 transition-all duration-300"
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
