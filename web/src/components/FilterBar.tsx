import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'

interface FilterBarProps {
  selectedEra: number | null
  onEraChange: (eraId: number | null) => void
  releaseStatus: string | null
  onStatusChange: (status: string | null) => void
}

export default function FilterBar({
  selectedEra,
  onEraChange,
  releaseStatus,
  onStatusChange,
}: FilterBarProps) {
  const { data: eras = [] } = useQuery({
    queryKey: ['eras'],
    queryFn: () => api.eras.list().then((res: any) => res.data),
  })

  return (
    <div className="mb-8 flex flex-wrap gap-4">
      <div>
        <label className="text-sm text-gray-400 block mb-2">Era</label>
        <select
          value={selectedEra || ''}
          onChange={(e) => onEraChange(e.target.value ? parseInt(e.target.value) : null)}
          className="px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 focus:border-blue-500 focus:outline-none transition"
        >
          <option value="">All Eras</option>
          {eras.map((era: any) => (
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
          onChange={(e) => onStatusChange(e.target.value || null)}
          className="px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 focus:border-blue-500 focus:outline-none transition"
        >
          <option value="">All Releases</option>
          <option value="released">Released</option>
          <option value="unreleased">Unreleased</option>
          <option value="unknown">Unknown</option>
        </select>
      </div>
    </div>
  )
}
