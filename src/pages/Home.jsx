import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 }
    }
  }

  return (
    <motion.div
      className="home-page"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >

      <motion.section variants={itemVariants} className="about-section">
        <h2>私たちについて</h2>
        <p>
          このサイトでは、会社をやめた「ゆか」と「ひろ」と、
          娘の3人の生活を発信しています。
          非日常の中から本当の「好き」を見つけ出す物語。
        </p>
      </motion.section>

      <motion.section variants={itemVariants} className="sns-section">
        <h2>SNS</h2>
        <p>各国の風景や文化をYouTube、Instagramで配信中！</p>
        <div className="sns-links">
          <motion.a
            href="https://www.youtube.com/@OurTripLife"
            target="_blank"
            rel="noopener noreferrer"
            className="sns-link youtube"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            📺 YouTubeチャンネルを見る
          </motion.a>
          <motion.a
            href="https://instagram.com/yuka_mama_triplife"
            target="_blank"
            rel="noopener noreferrer"
            className="sns-link instagram"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            📷 Instagramを見る
          </motion.a>
        </div>
      </motion.section>

      <motion.section variants={itemVariants} className="map-preview-section">
        <h2>世界一周の軌跡</h2>
        <p>
          2025/06~2026/02　家族で世界一周。
          訪れた国を地図にまとめています。ピンをクリックすると、
          その場所に関連するYouTubeをみることができます。
        </p>
        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Link to="/map" className="map-link-button">
            地図を見る →
          </Link>
        </motion.div>
      </motion.section>

      <motion.section variants={itemVariants} className="Nagano-section">
        <h2>長野移住</h2>
        <p>
          世界一周修了後は長野移住し、
          子連れ家族に優しいゲストハウスを運営予定。
        </p>
      </motion.section>

    </motion.div>




  )
}

export default Home

