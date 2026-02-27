export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-navy-950 pt-20 pb-8">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="grid md:grid-cols-12 gap-12 mb-16">
          {/* Logo & Description */}
          <div className="md:col-span-5">
            <div className="flex items-center gap-3 mb-5">
              <img
                src="./logo.png"
                alt="APEX Industries Group"
                className="h-10 w-auto"
              />
              <div>
                <span className="text-white font-semibold text-lg tracking-wider block leading-tight">APEX</span>
                <span className="text-gold-400 text-[10px] block tracking-[0.3em] uppercase leading-tight">Industries Group</span>
              </div>
            </div>
            <p className="text-white/35 text-sm leading-relaxed max-w-sm">
              Industrielle Unternehmensgruppe mit fünf spezialisierten Divisionen.
              Kompetenz, Struktur und Vertrauen seit über 25 Jahren.
            </p>
          </div>

          {/* Quick Links */}
          <div className="md:col-span-3 md:col-start-7">
            <h4 className="text-gold-400 text-[11px] font-semibold tracking-[0.2em] uppercase mb-5">Navigation</h4>
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
                    className="text-white/35 text-sm hover:text-gold-400 transition-colors duration-300"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div className="md:col-span-3">
            <h4 className="text-gold-400 text-[11px] font-semibold tracking-[0.2em] uppercase mb-5">Rechtliches</h4>
            <ul className="space-y-3">
              {['Impressum', 'Datenschutz', 'AGB', 'Cookie-Einstellungen'].map((item) => (
                <li key={item}>
                  <a
                    href="#"
                    className="text-white/35 text-sm hover:text-gold-400 transition-colors duration-300"
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-white/25 text-xs tracking-wide">
            &copy; {currentYear} APEX Industries Group. Alle Rechte vorbehalten.
          </p>
          <p className="text-white/15 text-xs tracking-wide">
            Design-Demo — Designkonzept
          </p>
        </div>
      </div>
    </footer>
  )
}
