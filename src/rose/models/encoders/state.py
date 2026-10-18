import torch
from torch import nn


class StateEncoder(nn.Module):
    def __init__(self, input_dim: int, output_dim: int = 128):
        super().__init__()
        self.network = nn.Sequential(nn.Linear(input_dim, output_dim), nn.SiLU(), nn.Linear(output_dim, output_dim))

    def forward(self, state):
        if state.shape[-1] != self.network[0].in_features:
            raise ValueError("state dimension mismatch")
        return self.network(state)
