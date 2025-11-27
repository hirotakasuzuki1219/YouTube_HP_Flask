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
    name: '東京',
    lat: 35.6762,
    lon: 139.6503,
    note: '出発地点',
    youtube: ''
  },
  {
    id: 2,
    name: 'パリ',
    lat: 48.8566,
    lon: 2.3522,
    note: 'フランスの首都',
    youtube: ''
  },
  {
    id: 3,
    name: 'ニューヨーク',
    lat: 40.7128,
    lon: -74.0060,
    note: 'アメリカの大都市',
    youtube: ''
  }
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

