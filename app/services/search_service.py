"""Search service with fuzzy matching."""
from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from app.models import Song
from app.repositories import SearchRepository


class SearchResult:
    """Search result with confidence score."""

    def __init__(self, song: Song, confidence: float) -> None:
        """Initialize search result."""
        self.song = song
        self.confidence = confidence

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.song.id,
            "title": self.song.title,
            "slug": self.song.slug,
            "release_status": self.song.release_status,
            "download_status": self.song.download_status,
            "official_url": self.song.official_url,
            "notes": self.song.notes,
            "era_id": self.song.era_id,
            "version_count": len(self.song.versions),
            "reference_count": len(self.song.references),
            "source_names": sorted(
                {
                    reference.source_name
                    for reference in self.song.references
                    if reference.source_name
                }
            ),
            "confidence": round(self.confidence, 2),
        }


class SearchService:
    """Service for searching songs with fuzzy matching."""

    FUZZY_THRESHOLD = 75

    def __init__(self, db: Session) -> None:
        """Initialize with database session."""
        self.db = db
        self.repo = SearchRepository(db)

    def search(self, query: str, skip: int = 0, limit: int = 50) -> list[SearchResult]:
        """Search songs with fuzzy matching fallback."""
        query = query.strip().lower()
        if not query:
            return []

        # Phase 1: Full-text search
        results = self.repo.full_text_search(query, skip=0, limit=100)
        if not results:
            results = self.db.query(Song).limit(100).all()

        # Phase 2: Score and rank results
        scored = self._score_results(query, results)

        # Phase 3: Filter by threshold
        above_threshold = [r for r in scored if r.confidence >= self.FUZZY_THRESHOLD]

        # Phase 4: Sort by confidence descending
        above_threshold.sort(key=lambda r: r.confidence, reverse=True)

        return above_threshold[skip : skip + limit]

    def _score_results(self, query: str, songs: list[Song]) -> list[SearchResult]:
        """Score songs by relevance to query."""
        results = []

        for song in songs:
            confidence = 0.0

            # Exact title match = 100
            if song.title.lower() == query:
                confidence = 100.0
            # Title contains query = 90
            elif query in song.title.lower():
                confidence = 90.0
            # Fuzzy match on title
            else:
                title_score = fuzz.partial_ratio(query, song.title.lower())
                confidence = max(confidence, title_score)

            # Check aliases
            for alias in song.aliases:
                if alias.alias.lower() == query:
                    confidence = 100.0
                    break
                alias_score = fuzz.partial_ratio(query, alias.alias.lower())
                confidence = max(confidence, alias_score)

            results.append(SearchResult(song, confidence))

        return results

    def search_by_lyrics(self, phrase: str, skip: int = 0, limit: int = 50) -> list[Song]:
        """Search by lyric snippets."""
        return self.repo.search_lyrics(phrase, skip=skip, limit=limit)

    def search_by_producer(self, producer_name: str, skip: int = 0, limit: int = 50) -> list[Song]:
        """Search by producer name."""
        return self.repo.search_by_producer(producer_name, skip=skip, limit=limit)

    def get_random_song(self, filters: dict | None = None) -> Song | None:
        """Get a random song with optional filters."""
        return self.repo.get_random_song(filters)
