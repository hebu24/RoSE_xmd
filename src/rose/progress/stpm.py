from rose.core.types import Observation, ProgressEstimate


class STPMProgressEstimator:
    def __init__(self, model, confidence: float | None = None):
        self.model = model
        self.confidence = confidence

    def estimate(self, observation: Observation) -> ProgressEstimate:
        value = self.model(observation)
        if hasattr(value, "item"):
            value = value.item()
        value = max(0.0, min(1.0, float(value)))
        return ProgressEstimate(value=value, confidence=self.confidence)
