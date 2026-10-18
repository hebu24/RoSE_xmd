import torch
from torch import nn


class VisualEncoder(nn.Module):
    def __init__(self, output_dim: int = 128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(3, 32, 5, stride=2, padding=2),
            nn.SiLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),
            nn.SiLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.projection = nn.Linear(64, output_dim)

    def forward(self, image):
        if image.ndim != 4 or image.shape[1] != 3:
            raise ValueError("image must have shape (B, 3, H, W)")
        return self.projection(self.network(image).flatten(1))
