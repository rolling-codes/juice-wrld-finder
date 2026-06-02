import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import DownloadButton from '../components/DownloadButton'
import type { DownloadLink, Song, SongReference, SongVersion } from '../types'

function versionTitle(version: SongVersion, fallback: string) {
  return version.title || fallback
}

function versionMeta(version: SongVersion) {
  return [version.version_type, version.release_status, version.source_name]
    .filter(Boolean)
    .join(' · ')
}

function isBaseVersion(version: SongVersion) {
  return version.is_base_version
}

function referenceTitle(reference: SongReference) {
  return reference.source_name
}

function actionKind(link: DownloadLink) {
  const value = `${link.link_type} ${link.label}`.toLowerCase()
  if (value.includes('official') || value.includes('stream') || value.includes('listen') || value.includes('audio')) {
    return 'listen'
  }
  if (value.includes('reference') || value.includes('source')) {
    return 'reference'
  }
  return 'download'
}

export default function SongDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const songId = id ? parseInt(id, 10) : null

  const { data: song, isLoading: songLoading } = useQuery<Song | null>({
    queryKey: ['song', songId],
    queryFn: () => (songId ? api.songs.get(songId).then((res) => res.data) : null),
    enabled: !!songId,
  })

  const { data: links = [] } = useQuery<DownloadLink[]>({
    queryKey: ['songLinks', songId],
    queryFn: () => (songId ? api.links.public(songId).then((res) => res.data) : []),
    enabled: !!songId,
  })

  const { data: versions = [] } = useQuery<SongVersion[]>({
    queryKey: ['songVersions', songId],
    queryFn: () => (songId ? api.songs.versions(songId).then((res) => res.data) : []),
    enabled: !!songId,
  })

  const { data: references = [] } = useQuery<SongReference[]>({
    queryKey: ['songReferences', songId],
    queryFn: () => (songId ? api.songs.references(songId).then((res) => res.data) : []),
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

  const baseVersion = versions.find(isBaseVersion) ?? versions[0]
  const listenLinks = links.filter((link) => actionKind(link) === 'listen')
  const referenceLinks = links.filter((link) => actionKind(link) === 'reference')
  const downloadLinks = links.filter((link) => actionKind(link) === 'download')

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

        {versions.length > 0 && (
          <div className="mb-8">
            <h3 className="text-sm text-gray-400 mb-4">Version Stack</h3>
            {baseVersion && (
              <div className="mb-4 rounded-lg border border-cyan-800 bg-cyan-950/40 p-4">
                <p className="text-xs uppercase tracking-wide text-cyan-300 mb-1">Base Version</p>
                <p className="font-semibold">{versionTitle(baseVersion, song.title)}</p>
                {baseVersion.notes && <p className="text-sm text-gray-300 mt-2">{baseVersion.notes}</p>}
              </div>
            )}
            <div className="space-y-3">
              {versions.map((version, index) => (
                <div key={version.id} className="rounded-lg border border-gray-700 bg-gray-900/60 p-4">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <p className="font-medium">{versionTitle(version, `Version ${index + 1}`)}</p>
                      {versionMeta(version) && <p className="text-sm text-gray-400 mt-1">{versionMeta(version)}</p>}
                    </div>
                    {isBaseVersion(version) && (
                      <span className="rounded bg-cyan-900 px-2 py-1 text-xs font-medium text-cyan-100">Base</span>
                    )}
                  </div>
                  {version.notes && <p className="text-sm text-gray-300 mt-3">{version.notes}</p>}
                </div>
              ))}
            </div>
          </div>
        )}

        {references.length > 0 && (
          <div className="mb-8">
            <h3 className="text-sm text-gray-400 mb-4">References</h3>
            <div className="overflow-x-auto rounded-lg border border-gray-700">
              <table className="w-full text-left text-sm">
                <thead className="bg-gray-900 text-gray-400">
                  <tr>
                    <th className="px-4 py-3 font-medium">Reference</th>
                    <th className="px-4 py-3 font-medium">Source</th>
                    <th className="px-4 py-3 font-medium">Type</th>
                    <th className="px-4 py-3 font-medium">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {references.map((reference) => (
                    <tr key={reference.id}>
                      <td className="px-4 py-3">
                        <p className="font-medium">{referenceTitle(reference)}</p>
                      {reference.description && <p className="text-gray-400 mt-1">{reference.description}</p>}
                    </td>
                      <td className="px-4 py-3 text-gray-300">{reference.source_name}</td>
                      <td className="px-4 py-3 text-gray-300">{reference.source_type}</td>
                      <td className="px-4 py-3">
                        {reference.source_url ? (
                          <a
                            href={reference.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-block rounded bg-gray-700 px-3 py-2 text-xs font-medium text-white transition hover:bg-gray-600"
                          >
                            Reference
                          </a>
                        ) : (
                          <span className="text-gray-500">-</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {listenLinks.length > 0 && (
          <div className="mb-8">
            <h3 className="text-sm text-gray-400 mb-4">Listen</h3>
            <div className="flex flex-wrap gap-3">
              {listenLinks.map((link) => (
                <DownloadButton key={link.id} link={link} />
              ))}
            </div>
          </div>
        )}

        {referenceLinks.length > 0 && (
          <div className="mb-8">
            <h3 className="text-sm text-gray-400 mb-4">Reference Actions</h3>
            <div className="flex flex-wrap gap-3">
              {referenceLinks.map((link) => (
                <DownloadButton key={link.id} link={link} />
              ))}
            </div>
          </div>
        )}

        {downloadLinks.length > 0 ? (
          <div>
            <h3 className="text-sm text-gray-400 mb-4">Download</h3>
            <div className="flex flex-wrap gap-3">
              {downloadLinks.map((link) => (
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
