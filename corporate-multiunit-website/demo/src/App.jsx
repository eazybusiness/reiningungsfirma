import Navbar from './components/Navbar'
import Hero from './components/Hero'
import About from './components/About'
import Stats from './components/Stats'
import Divisions from './components/Divisions'
import Contact from './components/Contact'
import Footer from './components/Footer'

function App() {
  return (
    <div className="min-h-screen bg-navy-950">
      <Navbar />
      <Hero />
      <About />
      <Stats />
      <Divisions />
      <Contact />
      <Footer />
    </div>
  )
}

export default App
