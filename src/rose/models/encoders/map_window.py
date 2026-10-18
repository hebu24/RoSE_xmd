import torch
import torch.nn as nn


class MAPWindowEncoder(nn.Module):
    def __init__(self, mode: str = "2d", action_dim: int = 7, output_dim: int = 128):
        super().__init__()
        if mode not in {"1d", "2d"}:
            raise ValueError("mode must be 1d or 2d")
        self.mode = mode
        self.action_dim = action_dim
        self.output_dim = output_dim
        if mode == "1d":
            self.network = nn.Sequential(
                nn.Conv1d(2, 32, 3, padding=1),
                nn.ReLU(),
                nn.Conv1d(32, 32, 3, padding=1),
                nn.ReLU(),
                nn.AdaptiveMaxPool1d(1),
            )
        else:
            self.network = nn.Sequential(
                nn.Conv2d(2, 32, 3, padding=1),
                nn.ReLU(),
                nn.Conv2d(32, 32, 3, padding=1),
                nn.ReLU(),
                nn.AdaptiveMaxPool2d((1, 1)),
            )
        self.projection = nn.Linear(32, output_dim)

    def forward(self, values, mask):
        if values.shape != mask.shape or values.shape[-1] != self.action_dim:
            raise ValueError("MAP values and mask must have shape (B, T, action_dim)")
        x = torch.stack((values, mask.to(dtype=values.dtype)), dim=1)
        if self.mode == "1d":
            x = x.permute(0, 1, 3, 2).reshape(values.shape[0] * self.action_dim, 2, values.shape[1])
            x = self.network(x).flatten(1).reshape(values.shape[0], self.action_dim, 32).flatten(1)
            return self.projection(x.reshape(values.shape[0], self.action_dim, 32).mean(dim=1))
        x = self.network(x).flatten(1)
        return self.projection(x)
