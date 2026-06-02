import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import SearchBar from '../components/SearchBar'
import FilterBar from '../components/FilterBar'
import SongCard from '../components/SongCard'
import type { Song } from '../types'

export default function Gallery() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedEra, setSelectedEra] = useState<number | null>(null)
  const [releaseStatus, setReleaseStatus] = useState<string | null>(null)
  const [versionFilter, setVersionFilter] = useState<string | null>(null)
  const [sourceFilter, setSourceFilter] = useState<string | null>(null)

  const { data: allSongs = [] } = useQuery<Song[]>({
    queryKey: ['songs', selectedEra, releaseStatus],
    queryFn: () =>
      api.songs
        .list(0, 100, selectedEra || undefined, releaseStatus || undefined)
        .then((res) => res.data),
  })

  const { data: searchResults = [], isLoading } = useQuery<Song[]>({
    queryKey: ['search', searchQuery],
    queryFn: () => api.search.query(searchQuery, 0, 50).then((res) => res.data),
    enabled: searchQuery.length > 0,
  })

  const sourceLabelsFor = (song: Song) => song.source_names ?? []
  const versionCountFor = (song: Song) => song.version_count ?? 0
  const referenceCountFor = (song: Song) => song.reference_count ?? 0

  const baseSongs = searchQuery.length > 0 ? searchResults : allSongs
  const supportsVersionFilter = baseSongs.some((song) => versionCountFor(song) > 0)
  const supportsSourceFilter = baseSongs.some((song) => sourceLabelsFor(song).length > 0 || referenceCountFor(song) > 0)
  const sourceOptions = Array.from(new Set(baseSongs.flatMap(sourceLabelsFor))).sort()
  const songs = baseSongs.filter((song) => {
    const versionCount = versionCountFor(song)
    const sourceLabels = sourceLabelsFor(song)

    if (versionFilter === 'has_versions' && versionCount < 2) {
      return false
    }

    if (versionFilter === 'base_only' && versionCount > 1) {
      return false
    }

    if (sourceFilter && !sourceLabels.includes(sourceFilter)) {
      return false
    }

    return true
  })

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

      {(supportsVersionFilter || supportsSourceFilter) && (
        <div className="mb-8 flex flex-wrap gap-4">
          {supportsVersionFilter && (
            <div>
              <label className="text-sm text-gray-400 block mb-2">Versions</label>
              <select
                value={versionFilter || ''}
                onChange={(e) => setVersionFilter(e.target.value || null)}
                className="px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 focus:border-blue-500 focus:outline-none transition"
              >
                <option value="">All Versions</option>
                <option value="has_versions">Has Versions</option>
                <option value="base_only">Base Only</option>
              </select>
            </div>
          )}

          {supportsSourceFilter && sourceOptions.length > 0 && (
            <div>
              <label className="text-sm text-gray-400 block mb-2">Source</label>
              <select
                value={sourceFilter || ''}
                onChange={(e) => setSourceFilter(e.target.value || null)}
                className="px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 focus:border-blue-500 focus:outline-none transition"
              >
                <option value="">All Sources</option>
                {sourceOptions.map((source) => (
                  <option key={source} value={source}>
                    {source}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      )}

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
