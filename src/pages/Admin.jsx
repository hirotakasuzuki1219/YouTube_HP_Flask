import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useAuth } from '../contexts/AuthContext'
import './Admin.css'

function Admin() {
  const { isAuthenticated } = useAuth()
  const [travels, setTravels] = useState([])
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    lat: '',
    lon: '',
    note: '',
    youtube: ''
  })
  const [message, setMessage] = useState({ text: '', type: '' })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (isAuthenticated) {
      loadTravels()
    }
  }, [isAuthenticated])

  const loadTravels = async () => {
    try {
      const response = await fetch('/api/travels', {
        credentials: 'include'
      })
      const data = await response.json()
      setTravels(data)
    } catch (error) {
      showMessage('データの取得に失敗しました: ' + error.message, 'error')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const submitData = {
        ...formData,
        lat: parseFloat(formData.lat),
        lon: parseFloat(formData.lon)
      }

      if (editingId) {
        const response = await fetch(`/api/travels/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(submitData)
        })
        if (response.ok) {
          showMessage('更新しました！', 'success')
          resetForm()
          loadTravels()
        }
      } else {
        const response = await fetch('/api/travels', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(submitData)
        })
        if (response.ok) {
          showMessage('追加しました！', 'success')
          resetForm()
          loadTravels()
        }
      }
    } catch (error) {
      showMessage('エラーが発生しました: ' + error.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = (travel) => {
    setFormData({
      name: travel.name,
      lat: travel.lat.toString(),
      lon: travel.lon.toString(),
      note: travel.note || '',
      youtube: travel.youtube || ''
    })
    setEditingId(travel.id)
  }

  const handleDelete = async (id) => {
    if (!window.confirm('本当に削除しますか？')) return

    try {
      const response = await fetch(`/api/travels/${id}`, {
        method: 'DELETE',
        credentials: 'include'
      })
      if (response.ok) {
        showMessage('削除しました！', 'success')
        loadTravels()
      }
    } catch (error) {
      showMessage('削除に失敗しました: ' + error.message, 'error')
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      lat: '',
      lon: '',
      note: '',
      youtube: ''
    })
    setEditingId(null)
  }

  const showMessage = (text, type) => {
    setMessage({ text, type })
    setTimeout(() => {
      setMessage({ text: '', type: '' })
    }, 3000)
  }

  return (
    <motion.div
      className="admin-page"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
    >
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="admin-header"
      >
        <h1>🌏 旅行データ管理</h1>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="admin-container"
      >
        <h2>新しい旅行地点を追加</h2>
        <form onSubmit={handleSubmit} className="travel-form">
          <div className="form-group">
            <label htmlFor="name">場所名 *</label>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="lat">緯度 (Latitude) *</label>
            <input
              type="number"
              id="lat"
              step="any"
              value={formData.lat}
              onChange={(e) => setFormData({ ...formData, lat: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="lon">経度 (Longitude) *</label>
            <input
              type="number"
              id="lon"
              step="any"
              value={formData.lon}
              onChange={(e) => setFormData({ ...formData, lon: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="note">メモ</label>
            <textarea
              id="note"
              value={formData.note}
              onChange={(e) => setFormData({ ...formData, note: e.target.value })}
              rows="4"
            />
          </div>
          <div className="form-group">
            <label htmlFor="youtube">YouTube埋め込みURL</label>
            <input
              type="text"
              id="youtube"
              value={formData.youtube}
              onChange={(e) => setFormData({ ...formData, youtube: e.target.value })}
              placeholder="https://www.youtube.com/embed/..."
            />
          </div>
          <div className="form-actions">
            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {editingId ? '更新' : '追加'}
            </motion.button>
            {editingId && (
              <motion.button
                type="button"
                onClick={resetForm}
                className="cancel-btn"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                キャンセル
              </motion.button>
            )}
          </div>
          <AnimatePresence>
            {message.text && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className={`message ${message.type}`}
              >
                {message.text}
              </motion.div>
            )}
          </AnimatePresence>
        </form>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="admin-container"
      >
        <h2>登録済みの旅行地点</h2>
        <AnimatePresence>
          {travels.length === 0 ? (
            <p>登録されている旅行地点がありません。</p>
          ) : (
            <div className="travel-list">
              {travels.map((travel, index) => (
                <motion.div
                  key={travel.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ delay: index * 0.1 }}
                  className="travel-item"
                >
                  <h3>{travel.name}</h3>
                  <p><strong>緯度:</strong> {travel.lat}, <strong>経度:</strong> {travel.lon}</p>
                  {travel.note && <p><strong>メモ:</strong> {travel.note}</p>}
                  {travel.youtube && (
                    <p>
                      <strong>YouTube:</strong>{' '}
                      <a href={travel.youtube} target="_blank" rel="noopener noreferrer">
                        {travel.youtube}
                      </a>
                    </p>
                  )}
                  <div className="travel-actions">
                    <motion.button
                      className="edit-btn"
                      onClick={() => handleEdit(travel)}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      編集
                    </motion.button>
                    <motion.button
                      className="delete-btn"
                      onClick={() => handleDelete(travel.id)}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      削除
                    </motion.button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  )
}

export default Admin

