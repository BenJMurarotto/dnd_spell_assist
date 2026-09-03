"""Fuzzy-matches transcript text against spell names — exact matching is too noisy since names like Light/Aid/Guidance are common words."""

from rapidfuzz import fuzz, process


class SpellMatcher:
    def __init__(self, spell_names: list[str], threshold: float = 85.0):
        self.spell_names = spell_names
        self.threshold = threshold

    def find_matches(self, transcript: str) -> list[str]:
        """Return spell names in transcript that score above the threshold."""
        results = process.extract(
            transcript,
            self.spell_names,
            scorer=fuzz.partial_ratio,
            score_cutoff=self.threshold,
            limit=None,
        )
        return [name for name, _, _ in results]
