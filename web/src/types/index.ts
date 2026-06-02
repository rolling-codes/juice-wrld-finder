export interface Song {
  id: number
  title: string
  slug: string
  release_status: string
  download_status: string
  official_url: string | null
  notes: string | null
  era_id: number | null
  version_count?: number
  reference_count?: number
  source_names?: string[]
}

export interface DownloadLink {
  id: number
  song_id: number
  label: string
  url: string
  link_type: string
  visibility: string
}

export interface SongVersion {
  id: number | null
  song_id: number
  title: string
  version_type: string
  release_status: string
  is_base_version: boolean
  recorded_date: string | null
  surfaced_date: string | null
  source_name: string | null
  source_url: string | null
  confidence: number
  sort_order: number
  notes: string | null
}

export interface SongReference {
  id: number
  song_id: number
  source_type: string
  source_name: string
  source_url: string | null
  description: string | null
  confidence: number
}

export interface Era {
  id: number
  name: string
}

export interface SearchResult extends Song {}
