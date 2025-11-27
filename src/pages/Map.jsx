import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import icon from 'leaflet/dist/images/marker-icon.png'
import iconShadow from 'leaflet/dist/images/marker-shadow.png'
import './Map.css'

// Leafletのデフォルトアイコンを設定
let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})
L.Marker.prototype.options.icon = DefaultIcon

// ハードコードされた旅行データ
// ここにピンのデータを追加・編集してください
const HARDCODED_TRAVELS = [
  {
    id: 1,
    name: '成田国際空港',
    lat: 35.776366,
    lon: 140.386249,
    note: 'ここから世界一周をスタート！まずはエジプトへ',
    youtube: 'https://www.youtube.com/embed/MsZmu32UglE'
  },
  {
    id: 2,
    name: 'エジプト・ギザ周辺',
    lat: 29.972883,
    lon: 31.128796,
    note: 'ピラミッド周辺を観光ツアーに参加',
    youtube: 'https://www.youtube.com/embed/_1sYoq9pQWg'
  },
  {
    id: 3,
    name: '大エジプト博物館',
    lat: 29.995239,
    lon: 31.119273,
    note: 'プレオープン中のレアな時期に潜入',
    youtube: 'https://www.youtube.com/embed/-6LvRT89h_k'
  },
  {
    id: 4,
    name: 'カイロ観光',
    lat: 30.046261,
    lon: 31.262404,
    note: 'アズハルモスクなどカイロ観光を堪能',
    youtube: 'https://www.youtube.com/embed/F1OhTilyzu0'
  },
  {
    id: 5,
    name: 'カイロ脱出',
    lat: 30.015892,
    lon: 31.224700,
    note: '閉じ込められて詰んだ',
    youtube: 'https://www.youtube.com/embed/k6KMBY0qDo8'
  },
  // ここに追加のピンを追加できます
]

function Map() {
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)
  const markersRef = useRef([])

  useEffect(() => {
    // 地図の初期化
    if (!mapInstanceRef.current && mapRef.current) {
      mapInstanceRef.current = L.map(mapRef.current).setView([35.776366, 140.386249], 1)

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap contributors'
      }).addTo(mapInstanceRef.current)
    }

    // ハードコードされたデータを使用
    const travels = HARDCODED_TRAVELS

    // 既存のマーカーを削除
    markersRef.current.forEach(marker => {
      mapInstanceRef.current.removeLayer(marker)
    })
    markersRef.current = []

    // 新しいマーカーを追加
    travels.forEach(travel => {
      const marker = L.marker([travel.lat, travel.lon])
        .addTo(mapInstanceRef.current)
        .bindPopup(
          `<div class="popup-content">
            <b>${travel.name}</b><br/>
            ${travel.note ? `<p>${travel.note}</p>` : ''}
            ${travel.youtube ? `<iframe width="200" height="113" src="${travel.youtube}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>` : ''}
          </div>`
        )
      markersRef.current.push(marker)
    })

    // データがある場合、地図をズーム
    if (travels.length > 0) {
      const bounds = L.latLngBounds(travels.map(t => [t.lat, t.lon]))
      mapInstanceRef.current.fitBounds(bounds, { padding: [50, 50] })
    }

    // クリーンアップ
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [])

  return (
    <motion.div
      className="map-page"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
    >
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="map-header"
      >
        <h2>世界一周の軌跡</h2>
        <p>ピンをクリックすると、その場所に関連するYouTubeをみることができます。</p>
      </motion.div>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
        className="map-container"
      >
        <div ref={mapRef} id="map" />
      </motion.div>
    </motion.div>
  )
}

export default Map

