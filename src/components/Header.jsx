import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import './Header.css'

function Header() {
  const location = useLocation()

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="header"
    >
      <motion.h1
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        🌏 ゆか＆ひろ（家族世界一周）
      </motion.h1>
      <nav>
        <Link
          to="/"
          className={location.pathname === '/' ? 'active' : ''}
        >
          ホーム
        </Link>
        <Link
          to="/map"
          className={location.pathname === '/map' ? 'active' : ''}
        >
          世界一周の軌跡
        </Link>
      </nav>
    </motion.header>
  )
}

export default Header

