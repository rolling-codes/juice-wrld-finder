import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import DownloadButton from '../components/DownloadButton'

export default function SongDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const songId = id ? parseInt(id, 10) : null

  const { data: song, isLoading: songLoading } = useQuery({
    queryKey: ['song', songId],
    queryFn: () => (songId ? api.songs.get(songId).then((res) => res.data) : null),
    enabled: !!songId,
  })

  const { data: links = [], isLoading: linksLoading } = useQuery({
    queryKey: ['songLinks', songId],
    queryFn: () => (songId ? api.links.public(songId).then((res) => res.data) : []),
    enabled: !!songId,
  })

  if (!songId) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-gray-400 mb-4">Song not found</p>
        <button
          onClick={() => navigate('/')}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition"
        >
          Back to Gallery
        </button>
      </div>
    )
  }

  if (songLoading) {
    return (
      <div className="flex justify-center py-12">
        <p className="text-gray-400">Loading song details...</p>
      </div>
    )
  }

  if (!song) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-gray-400 mb-4">Song not found</p>
        <button
          onClick={() => navigate('/')}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition"
        >
          Back to Gallery
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto">
      <button
        onClick={() => navigate('/')}
        className="mb-6 px-3 py-2 text-sm text-gray-400 hover:text-white transition"
      >
        ← Back
      </button>

      <div className="bg-gray-800 rounded-lg p-8 border border-gray-700">
        <h1 className="text-4xl font-bold mb-4">{song.title}</h1>

        <div className="grid grid-cols-2 gap-6 mb-8">
          <div>
            <h3 className="text-sm text-gray-400 mb-2">Release Status</h3>
            <p className="text-lg capitalize">{song.release_status}</p>
          </div>
          <div>
            <h3 className="text-sm text-gray-400 mb-2">Download Status</h3>
            <p className="text-lg capitalize">{song.download_status}</p>
          </div>
        </div>

        {song.notes && (
          <div className="mb-8">
            <h3 className="text-sm text-gray-400 mb-2">Notes</h3>
            <p className="text-gray-300">{song.notes}</p>
          </div>
        )}

        {song.official_url && (
          <div className="mb-8">
            <h3 className="text-sm text-gray-400 mb-2">Official Link</h3>
            <a
              href={song.official_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 transition break-all"
            >
              {song.official_url}
            </a>
          </div>
        )}

        {links.length > 0 ? (
          <div>
            <h3 className="text-sm text-gray-400 mb-4">Download Links</h3>
            <div className="flex flex-wrap gap-3">
              {links.map((link) => (
                <div key={link.id} className="flex gap-2">
                  <DownloadButton link={link} />
                  <a
                    href={`/api/downloads/${songId}?link_id=${link.id}`}
                    className="inline-block px-3 py-2 rounded text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition"
                    title="Download via API"
                  >
                    ↓
                  </a>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-gray-400 text-sm">No download links available for this song</p>
        )}
      </div>
    </div>
  )
}
