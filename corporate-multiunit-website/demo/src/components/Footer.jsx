export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-navy-950 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-12 mb-16">
          {/* Logo & Description */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 border-2 border-gold-400 flex items-center justify-center">
                <span className="text-gold-400 font-serif font-bold text-lg">A</span>
              </div>
              <div>
                <span className="text-white font-semibold text-lg tracking-wide">APEX</span>
                <span className="text-gold-400 text-xs block tracking-[0.25em] uppercase">Industries Group</span>
              </div>
            </div>
            <p className="text-navy-400 text-sm leading-relaxed max-w-sm">
              Industrielle Unternehmensgruppe mit fünf spezialisierten Divisionen.
              Kompetenz, Struktur und Vertrauen seit über 25 Jahren.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-gold-400 text-sm font-semibold tracking-wide uppercase mb-4">Navigation</h4>
            <ul className="space-y-3">
              {[
                { label: 'Startseite', href: '#hero' },
                { label: 'Über uns', href: '#about' },
                { label: 'Divisionen', href: '#divisions' },
                { label: 'Kontakt', href: '#contact' },
              ].map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    className="text-navy-400 text-sm hover:text-gold-400 transition-colors duration-300"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-gold-400 text-sm font-semibold tracking-wide uppercase mb-4">Rechtliches</h4>
            <ul className="space-y-3">
              {['Impressum', 'Datenschutz', 'AGB', 'Cookie-Einstellungen'].map((item) => (
                <li key={item}>
                  <a
                    href="#"
                    className="text-navy-400 text-sm hover:text-gold-400 transition-colors duration-300"
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-navy-800 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-navy-500 text-xs">
            &copy; {currentYear} APEX Industries Group. Alle Rechte vorbehalten.
          </p>
          <p className="text-navy-600 text-xs">
            Design-Demo — Nicht die endgültige Website
          </p>
        </div>
      </div>
    </footer>
  )
}
