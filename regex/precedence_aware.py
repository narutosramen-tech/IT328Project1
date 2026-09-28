class PrecedenceAware:
    def compare(self, other: 'PrecedenceAware') -> int:
        raise NotImplementedError("Subclasses must implement compare method.")