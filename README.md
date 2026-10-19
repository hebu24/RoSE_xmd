# RoSE

RoSE is a unified MAP/IP framework for ManiSkill, LIBERO/LeRobot, and Franka
workflows. The simulator and robot projects are external integrations; they
are not vendored into `third_party/`.

## One-command setup

Install `uv`, clone this repository, and run:

```bash
git clone https://github.com/hebu24/RoSE_xmd.git
cd RoSE_xmd
bash scripts/setup_env.sh
```

The command creates `.venv`, installs RoSE with the `all` dependency profile,
installs ManiSkill and LeRobot from the default sibling paths when they exist,
runs `uv pip check`, import checks, and the test suite. It is safe to run again;
`uv` reuses the environment and only updates what is needed.

The default profile uses Python 3.12 because the current LeRobot integration
requires Python >=3.12 and the ManiSkill `mplib` dependency currently has no
Python 3.13 wheel. A minimal environment for unit tests can
be created with:

```bash
bash scripts/setup_env.sh --profile core --no-external
```

Other profiles are `sim` (PyTorch, ManiSkill/LIBERO dependencies) and `real`
(PyTorch and Franka data dependencies). Use `--python 3.12` or
`--venv /path/to/venv` to select them explicitly. Add `--no-external` when the
external repositories are not available locally.

## External repositories

The setup command looks for:

```text
$HOME/code/mam/ManiSkill
$HOME/code/mam/lerobot_mam
```

Override these locations before setup if needed:

```bash
export ROSE_MANISKILL_ROOT=/path/to/ManiSkill
export ROSE_LEROBOT_ROOT=/path/to/lerobot_mam
export ROSE_MASKED_ACTION_ROOT=/path/to/Masked-Action-Model
bash scripts/setup_env.sh
```

`Masked-Action-Model` is a source-only integration and is checked by the
runtime when its commands are used. The setup script does not copy external
source into this repository.

## Running and diagnosing

After setup, activate the environment or let the scripts automatically use
`.venv`:

```bash
source .venv/bin/activate
bash scripts/eval_ip_maniskill.sh --dry-run
bash scripts/eval_ip_libero.sh --dry-run
bash scripts/infer_ip_franka.sh --dry-run
```

`setup_env.sh` fails on a dependency conflict (`uv pip check`), failed imports,
or failed tests. A missing NVIDIA driver is reported by the PyTorch check but
does not prevent CPU installation; GPU simulation still requires a working
driver and compatible CUDA runtime.

## Repository layout

- `src/rose/core`: contracts, interfaces, configuration, and shared types.
- `src/rose/data`: datasets, masks, MAP windows, normalization, and action spaces.
- `src/rose/envs`: environment adapters for ManiSkill, LIBERO, and Franka.
- `src/rose/integrations`: external repository discovery and command builders.
- `src/rose/models`: IP, diffusion, RePaint, and encoder modules.
- `src/rose/progress`: progress estimators and window construction.
- `src/rose/runtimes` and `src/rose/cli`: train/evaluate/infer/preprocess entry points.
- `configs`: shared, simulation, and real-robot YAML configurations.
- `scripts`: reproducible command wrappers.
