export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-navy-950 border-t border-white/[0.06]">
      <div className="max-w-[1200px] mx-auto px-6 lg:px-10">

        {/* Main footer content */}
        <div className="py-16 lg:py-20 grid md:grid-cols-12 gap-12">
          {/* Logo & tagline */}
          <div className="md:col-span-5">
            <div className="flex items-center gap-3 mb-5">
              <img src="./logo.png" alt="APEX Industries Group" className="h-8 w-auto" />
              <span className="text-white font-semibold text-[15px] tracking-wider">APEX</span>
            </div>
            <p className="text-white/30 text-[13px] leading-[1.7] max-w-xs">
              Industrielle Unternehmensgruppe mit fünf spezialisierten
              Divisionen. Frankfurt am Main, Deutschland.
            </p>
          </div>

          {/* Navigation */}
          <div className="md:col-span-3 md:col-start-7">
            <ul className="space-y-3">
              {[
                { label: 'Über uns', href: '#about' },
                { label: 'Divisionen', href: '#divisions' },
                { label: 'Kontakt', href: '#contact' },
              ].map((link) => (
                <li key={link.href}>
                  <a href={link.href} className="text-white/30 text-[13px] hover:text-white/60 transition-colors duration-300">
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div className="md:col-span-2">
            <ul className="space-y-3">
              {['Impressum', 'Datenschutz', 'AGB'].map((item) => (
                <li key={item}>
                  <a href="#" className="text-white/30 text-[13px] hover:text-white/60 transition-colors duration-300">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom line */}
        <div className="border-t border-white/[0.06] py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-white/20 text-[11px]">
            &copy; {currentYear} APEX Industries Group
          </p>
          <p className="text-white/10 text-[11px]">
            Designkonzept
          </p>
        </div>
      </div>
    </footer>
  )
}
