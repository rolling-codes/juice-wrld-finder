export interface Song {
  id: number
  title: string
  slug: string
  release_status: string
  download_status: string
  official_url: string | null
  notes: string | null
  era_id: number | null
}

export interface DownloadLink {
  id: number
  song_id: number
  label: string
  url: string
  link_type: string
  visibility: string
}

export interface Era {
  id: number
  name: string
}

export interface SearchResult extends Song {}
