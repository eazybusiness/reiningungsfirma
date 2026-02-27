import Navbar from './components/Navbar'
import Hero from './components/Hero'
import About from './components/About'
import Mission from './components/Mission'
import Divisions from './components/Divisions'
import Contact from './components/Contact'
import Footer from './components/Footer'

function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <About />
      <Mission />
      <Divisions />
      <Contact />
      <Footer />
    </div>
  )
}

export default App
