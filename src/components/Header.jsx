import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Menu, X, Phone, Mail, Sparkles } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navigation = [
    { name: 'Startseite', href: '/' },
    { name: 'Leistungen', href: '/leistungen' },
    { name: 'Kontakt', href: '/kontakt' },
  ]

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-20 items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">CleanPro</span>
          </Link>

          <div className="hidden md:flex md:items-center md:space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
              >
                {item.name}
              </Link>
            ))}
            <div className="flex items-center space-x-4 pl-4 border-l border-gray-200">
              <a href="tel:+491234567890" className="flex items-center text-sm text-gray-600 hover:text-blue-600">
                <Phone className="h-4 w-4 mr-1" />
                <span className="hidden lg:inline">+49 123 456 7890</span>
              </a>
              <a
                href="#kontakt"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Angebot anfordern
              </a>
            </div>
          </div>

          <button
            type="button"
            className="md:hidden p-2 rounded-lg text-gray-700 hover:bg-gray-100"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </nav>

      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-gray-200 bg-white"
          >
            <div className="px-4 py-4 space-y-3">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              <div className="pt-3 border-t border-gray-200 space-y-2">
                <a
                  href="tel:+491234567890"
                  className="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg"
                >
                  <Phone className="h-4 w-4 mr-2" />
                  +49 123 456 7890
                </a>
                <a
                  href="#kontakt"
                  className="block bg-blue-600 text-white px-4 py-2 rounded-lg text-center font-medium"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Angebot anfordern
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
