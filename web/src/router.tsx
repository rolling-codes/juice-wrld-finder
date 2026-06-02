import { Routes, Route } from 'react-router-dom'
import Gallery from './pages/Gallery'
import SongDetail from './pages/SongDetail'

export default function Router() {
  return (
    <Routes>
      <Route path="/" element={<Gallery />} />
      <Route path="/songs/:id" element={<SongDetail />} />
    </Routes>
  )
}
