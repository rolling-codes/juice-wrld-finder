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

function getVersionCount(song: Song): number | null {
  return song.version_count ?? null
}

function getReferenceCount(song: Song): number | null {
  return song.reference_count ?? null
}

function getSourceLabels(song: Song): string[] {
  return song.source_names ?? []
}

export default function SongCard({ song }: SongCardProps) {
  const statusColor = releaseStatusColor[song.release_status.toLowerCase()] || releaseStatusColor.unknown
  const versionCount = getVersionCount(song)
  const referenceCount = getReferenceCount(song)
  const sourceLabels = getSourceLabels(song)

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
          {versionCount !== null && (
            <span className="inline-block px-2 py-1 rounded text-xs font-medium bg-cyan-900 text-cyan-100">
              {versionCount} {versionCount === 1 ? 'version' : 'versions'}
            </span>
          )}
          {referenceCount !== null && (
            <span className="inline-block px-2 py-1 rounded text-xs font-medium bg-indigo-900 text-indigo-100">
              {referenceCount} {referenceCount === 1 ? 'source' : 'sources'}
            </span>
          )}
        </div>
        {sourceLabels.length > 0 && (
          <p className="text-xs text-gray-500 mb-2 line-clamp-1">
            Sources: {sourceLabels.join(', ')}
          </p>
        )}
        {song.notes && (
          <p className="text-sm text-gray-400 line-clamp-2">{song.notes}</p>
        )}
      </div>
    </Link>
  )
}
