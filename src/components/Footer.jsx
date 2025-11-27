import { motion } from 'framer-motion'
import './Footer.css'

function Footer() {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.3, duration: 0.5 }}
      className="footer"
    >
      <p>&copy; 2025 Our Trip Life</p>
    </motion.footer>
  )
}

export default Footer





