import { Link } from 'react-router-dom'
import { Phone, Mail, MapPin, Sparkles } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">CleanPro</span>
            </div>
            <p className="text-sm text-gray-400">
              Professionelle Reinigungsdienstleistungen für Büros, Praxen und Privathaushalte.
            </p>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Navigation</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/" className="hover:text-white transition-colors">Startseite</Link></li>
              <li><Link to="/leistungen" className="hover:text-white transition-colors">Leistungen</Link></li>
              <li><Link to="/kontakt" className="hover:text-white transition-colors">Kontakt</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Leistungen</h3>
            <ul className="space-y-2 text-sm">
              <li><span className="hover:text-white transition-colors cursor-pointer">Büroreinigung</span></li>
              <li><span className="hover:text-white transition-colors cursor-pointer">Privatreinigung</span></li>
              <li><span className="hover:text-white transition-colors cursor-pointer">Fensterreinigung</span></li>
              <li><span className="hover:text-white transition-colors cursor-pointer">Grundreinigung</span></li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Kontakt</h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start">
                <Phone className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                <a href="tel:+491234567890" className="hover:text-white transition-colors">
                  +49 123 456 7890
                </a>
              </li>
              <li className="flex items-start">
                <Mail className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                <a href="mailto:info@cleanpro.de" className="hover:text-white transition-colors">
                  info@cleanpro.de
                </a>
              </li>
              <li className="flex items-start">
                <MapPin className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                <span>Musterstraße 123<br />12345 Berlin</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-800 flex flex-col sm:flex-row justify-between items-center text-sm">
          <p>&copy; 2026 CleanPro. Alle Rechte vorbehalten.</p>
          <div className="flex space-x-6 mt-4 sm:mt-0">
            <Link to="/impressum" className="hover:text-white transition-colors">Impressum</Link>
            <Link to="/datenschutz" className="hover:text-white transition-colors">Datenschutz</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
