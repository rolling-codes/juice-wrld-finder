import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import SearchBar from '../components/SearchBar'
import SongCard from '../components/SongCard'
import { Song } from '../types'

export default function Gallery() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedEra, setSelectedEra] = useState<number | null>(null)
  const [releaseStatus, setReleaseStatus] = useState<string | null>(null)

  // Fetch all eras for filter
  const { data: eras = [] } = useQuery({
    queryKey: ['eras'],
    queryFn: () => api.eras.list().then((res) => res.data),
  })

  // Fetch all songs with filters
  const { data: allSongs = [], isLoading } = useQuery({
    queryKey: ['songs', selectedEra, releaseStatus],
    queryFn: () => api.songs.list(0, 100, selectedEra || undefined, releaseStatus || undefined).then((res) => res.data),
  })

  // Fetch search results
  const { data: searchResults = [] } = useQuery({
    queryKey: ['search', searchQuery],
    queryFn: () => api.search.query(searchQuery, 0, 50).then((res) => res.data),
    enabled: searchQuery.length > 0,
  })

  // Determine which songs to display
  const displayedSongs = useMemo<Song[]>(() => {
    if (searchQuery.length > 0) {
      return searchResults
    }
    return allSongs
  }, [searchQuery, allSongs, searchResults])

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Juice WRLD Songs</h1>
        <p className="text-gray-400">Browse and discover songs by era, release status, and more</p>
      </div>

      <SearchBar onSearch={setSearchQuery} />

      <div className="mb-8 flex flex-wrap gap-4">
        <div>
          <label className="text-sm text-gray-400 block mb-2">Era</label>
          <select
            value={selectedEra || ''}
            onChange={(e) => setSelectedEra(e.target.value ? parseInt(e.target.value) : null)}
            className="px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 focus:border-blue-500 focus:outline-none transition"
          >
            <option value="">All Eras</option>
            {eras.map((era) => (
              <option key={era.id} value={era.id}>
                {era.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="text-sm text-gray-400 block mb-2">Release Status</label>
          <select
            value={releaseStatus || ''}
            onChange={(e) => setReleaseStatus(e.target.value || null)}
            className="px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 focus:border-blue-500 focus:outline-none transition"
          >
            <option value="">All Releases</option>
            <option value="released">Released</option>
            <option value="unreleased">Unreleased</option>
            <option value="unknown">Unknown</option>
          </select>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <p className="text-gray-400">Loading...</p>
        </div>
      ) : displayedSongs.length === 0 ? (
        <div className="flex justify-center py-12">
          <p className="text-gray-400">
            {searchQuery ? 'No songs found matching your search' : 'No songs available'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {displayedSongs.map((song) => (
            <SongCard key={song.id} song={song} />
          ))}
        </div>
      )}
    </div>
  )
}
