import { Link } from 'react-router-dom'
import { Song } from '../types'

interface SongCardProps {
  song: Song
}

const releaseStatusColor: Record<string, string> = {
  released: 'bg-green-900 text-green-200',
  unreleased: 'bg-yellow-900 text-yellow-200',
  unknown: 'bg-gray-700 text-gray-200',
}

export default function SongCard({ song }: SongCardProps) {
  const statusColor = releaseStatusColor[song.release_status.toLowerCase()] || releaseStatusColor.unknown

  return (
    <Link to={`/songs/${song.id}`}>
      <div className="bg-gray-800 rounded-lg p-4 hover:bg-gray-750 transition cursor-pointer border border-gray-700 hover:border-gray-600">
        <h3 className="text-lg font-semibold mb-2 line-clamp-2">{song.title}</h3>
        <div className="flex flex-wrap gap-2 mb-3">
          <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${statusColor}`}>
            {song.release_status}
          </span>
          {song.era_id && (
            <span className="inline-block px-2 py-1 rounded text-xs font-medium bg-blue-900 text-blue-200">
              Era {song.era_id}
            </span>
          )}
        </div>
        {song.notes && (
          <p className="text-sm text-gray-400 line-clamp-2">{song.notes}</p>
        )}
      </div>
    </Link>
  )
}
