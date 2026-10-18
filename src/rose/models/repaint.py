import numpy as np


def overwrite_known(proposal, reference, mask):
    if proposal.shape != reference.shape or mask.shape != proposal.shape:
        raise ValueError("proposal, reference, and mask must have the same shape")
    if isinstance(proposal, np.ndarray):
        return np.where(mask.astype(bool), reference, proposal)
    import torch

    return torch.where(mask.to(device=proposal.device, dtype=torch.bool), reference, proposal)


def repaint_step(proposal, reference_noisy, mask):
    return overwrite_known(proposal, reference_noisy, mask)


def reference_at_noise_level(reference, mask, alpha_bar, noise=None):
    if isinstance(reference, np.ndarray):
        if noise is None:
            noise = np.zeros_like(reference)
        return overwrite_known(
            np.zeros_like(reference),
            alpha_bar**0.5 * reference + (1.0 - alpha_bar) ** 0.5 * noise,
            mask,
        )
    import torch

    if noise is None:
        noise = torch.zeros_like(reference)
    return overwrite_known(
        torch.zeros_like(reference),
        alpha_bar**0.5 * reference + (1.0 - alpha_bar) ** 0.5 * noise,
        mask,
    )
