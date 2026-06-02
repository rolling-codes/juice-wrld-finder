import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import SearchBar from '../components/SearchBar'
import FilterBar from '../components/FilterBar'
import SongCard from '../components/SongCard'
import { Song } from '../types'

export default function Gallery() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedEra, setSelectedEra] = useState<number | null>(null)
  const [releaseStatus, setReleaseStatus] = useState<string | null>(null)

  const { data: allSongs = [] as Song[] } = useQuery({
    queryKey: ['songs', selectedEra, releaseStatus],
    queryFn: () =>
      api.songs
        .list(0, 100, selectedEra || undefined, releaseStatus || undefined)
        .then((res: any) => res.data),
  })

  const { data: searchResults = [] as Song[], isLoading } = useQuery({
    queryKey: ['search', searchQuery],
    queryFn: () => api.search.query(searchQuery, 0, 50).then((res: any) => res.data),
    enabled: searchQuery.length > 0,
  })

  const songs = searchQuery.length > 0 ? searchResults : allSongs

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Juice WRLD Songs</h1>
        <p className="text-gray-400">Browse and discover songs by era, release status, and more</p>
      </div>

      <SearchBar onSearch={setSearchQuery} />
      <FilterBar
        selectedEra={selectedEra}
        onEraChange={setSelectedEra}
        releaseStatus={releaseStatus}
        onStatusChange={setReleaseStatus}
      />

      {isLoading ? (
        <div className="flex justify-center py-12">
          <p className="text-gray-400">Loading...</p>
        </div>
      ) : songs.length === 0 ? (
        <div className="flex justify-center py-12">
          <p className="text-gray-400">
            {searchQuery ? 'No songs found matching your search' : 'No songs available'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {songs.map((song) => (
            <SongCard key={song.id} song={song} />
          ))}
        </div>
      )}
    </div>
  )
}
