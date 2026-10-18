from dataclasses import dataclass


@dataclass(frozen=True)
class IPConfig:
    policy_name: str = "IP"
    action_dim: int = 7
    known_weight: float = 1.0
    unknown_weight: float = 1.0


def weighted_noise_loss(noise, prediction, mask, known_weight: float = 1.0, unknown_weight: float = 1.0):
    import torch

    if noise.shape != prediction.shape or mask.shape != noise.shape:
        raise ValueError("noise, prediction, and mask must have the same shape")
    weights = mask.to(dtype=noise.dtype) * known_weight + (1.0 - mask.to(dtype=noise.dtype)) * unknown_weight
    return ((noise - prediction).square() * weights).mean()


class IP:
    name = "IP"

    def __init__(self, denoiser, config: IPConfig | None = None):
        self.denoiser = denoiser
        self.config = config or IPConfig()

    def predict_noise(self, noisy_action, timestep, observation, map_window):
        return self.denoiser(noisy_action, timestep, observation, map_window)

    def loss(self, noise, prediction, mask):
        return weighted_noise_loss(
            noise,
            prediction,
            mask,
            known_weight=self.config.known_weight,
            unknown_weight=self.config.unknown_weight,
        )
