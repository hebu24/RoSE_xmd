from rose.core.types import Observation, ProgressEstimate


class CallableProgressEstimator:
    def __init__(self, model):
        self.model = model

    def estimate(self, observation: Observation) -> ProgressEstimate:
        value = float(self.model(observation))
        return ProgressEstimate(value=max(0.0, min(1.0, value)))
