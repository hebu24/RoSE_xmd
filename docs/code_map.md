# 旧代码到新框架的映射

这里只记录迁移边界，不复制旧文件。

| 新模块 | ManiSkill / MAM 来源 | LIBERO 来源 | Franka 来源 |
|---|---|---|---|
| `data/adapters` | `ManiSkill/sft_data_generation/gen_mam_training_arr.py`、`Masked-Action-Model/.../data_preprocess/` | `lerobot_mam/src/lerobot/datasets/`、`scripts/libero/` | `franka_train/preprocess_franka.py`、`dataset_umi.py` |
| `data/masks.py` | `Masked-Action-Model/.../data_preprocess/utils/mask_utils.py` | `lerobot_mam/src/lerobot/policies/mam/processor_mam.py` | `franka_train/preprocess_franka.py` 中的 mask 配置 |
| `models/policy.py` | `.../models/modeling_ditdp.py`、`conditional_unet1d.py` | `lerobot_mam/src/lerobot/policies/mam/modeling_mam.py` | `franka_train/train_mam_franka*.py` 使用的 policy 配置 |
| `models/encoders/map.py` | `.../models/mas_conv1d.py`、`mas_conv2d.py` | `lerobot_mam/src/lerobot/policies/mam/` | 真机沿用同一 MAP contract |
| `models/repaint.py` | `.../utils/inpainting_utils.py`、`eval_inpaint.py` | 后续接入 LIBERO inference | 后续接入真机 inference |
| `progress/window.py` | `.../utils/progress_utils.py` | STPM/MAM processor | `franka_train` 的 progress/MAS 配置 |
| `progress/estimator.py` | `STPM/` | `lerobot_mam/src/lerobot/stpm/` | `STPM` 真机训练入口 |
| `envs/maniskill.py` | `.../utils/make_env.py`、`evaluate/evaluate_mam.py` | — | — |
| `envs/libero.py` | — | `src/lerobot/envs/libero.py`、`scripts/libero/` | — |
| `envs/franka.py` | — | — | `franka_train` 与 `mam-realworld-infer/` |
| `runtimes/trainer.py` | `train_mam.py`、`train_baseline.py` | `src/lerobot/scripts/lerobot_train.py`、LIBERO launch scripts | `train_mam_franka*.py` |
| `runtimes/evaluator.py` | `evaluate/evaluate_mam.py`、`eval_ce.py` | LIBERO eval scripts | offline chunk validation |
| `cli/*` | `run_mam.sh`、`run_eval_inpaint.sh` | `scripts/launch_mam*` | `run_train_mam_franka*.sh` |

## 外部依赖策略

新仓库不把三个旧仓库当作 git submodule，也不把它们的全部源码复制进来。adapter 通过 `ROSE_MANISKILL_ROOT`、`ROSE_MASKED_ACTION_ROOT`、`ROSE_LEROBOT_ROOT` 解析外部源码；以后某个实现稳定后，再逐文件迁入 `src/rose_xmd`。
