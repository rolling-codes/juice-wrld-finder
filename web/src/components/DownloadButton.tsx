import { DownloadLink } from '../types'

interface DownloadButtonProps {
  link: DownloadLink
}

const linkTypeColors: Record<string, string> = {
  mega: 'bg-purple-600 hover:bg-purple-700',
  api: 'bg-blue-600 hover:bg-blue-700',
  official: 'bg-green-600 hover:bg-green-700',
  other: 'bg-gray-600 hover:bg-gray-700',
}

export default function DownloadButton({ link }: DownloadButtonProps) {
  const colorClass = linkTypeColors[link.link_type.toLowerCase()] || linkTypeColors.other

  return (
    <a
      href={link.url}
      target="_blank"
      rel="noopener noreferrer"
      className={`inline-block px-3 py-2 rounded text-sm font-medium text-white transition ${colorClass}`}
      title={`${link.link_type} - ${link.label}`}
    >
      {link.label}
    </a>
  )
}
