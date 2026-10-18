from dataclasses import dataclass


@dataclass(frozen=True)
class DiffusionConfig:
    steps: int = 100
    beta_start: float = 1e-4
    beta_end: float = 2e-2


def linear_betas(config: DiffusionConfig):
    import torch

    if config.steps < 1 or config.beta_start <= 0 or config.beta_end <= config.beta_start:
        raise ValueError("invalid diffusion schedule")
    return torch.linspace(config.beta_start, config.beta_end, config.steps)


def add_noise(values, noise, timestep, config: DiffusionConfig):
    import torch

    betas = linear_betas(config).to(device=values.device, dtype=values.dtype)
    alpha_bar = torch.cumprod(1.0 - betas, dim=0)
    index = torch.as_tensor(timestep, device=values.device, dtype=torch.long)
    scale = alpha_bar[index].sqrt().reshape((-1,) + (1,) * (values.ndim - 1))
    residual = (1.0 - alpha_bar[index]).sqrt().reshape((-1,) + (1,) * (values.ndim - 1))
    return scale * values + residual * noise
