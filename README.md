# RoSE_xmd

Robotic Spatiotemporal Editing 的统一代码框架。

本仓库用于统一三条现有代码链路：

- ManiSkill 仿真：数据生成、MAM/DiT 训练、仿真 rollout 与 control error 评估。
- LIBERO 仿真：LeRobot 数据集、语言条件多任务训练、STPM progress 和 LIBERO 评估。
- Franka 真机：H5/LeRobot 数据预处理、MAM/DP/STPM 训练以及硬件侧 inference。

当前提交是**框架设计版本**：只建立目录、接口边界、配置和迁移映射，不复制旧仓库实现，也不修改旧仓库。

## 设计原则

1. `src/rose_xmd` 只放跨平台的核心协议、数据结构、模型编排和运行时流程。
2. `src/rose_xmd/integrations` 负责接入 ManiSkill、LeRobot/LIBERO 和 Franka，不让核心模块直接依赖某一个平台。
3. `third_party/` 只记录外部源码位置和版本，不把三个大型仓库嵌套复制进来。
4. 训练、评估、预处理和真机 inference 共用同一套 MAP、mask、progress、window 和 action contract。
5. 平台差异通过 adapter/backend 解决，配置通过 `configs/` 和命令行覆盖。

## 目录

```text
RoSE_xmd/
├── configs/                  # 跨平台、仿真、真机配置
├── docs/                     # 架构、迁移映射、运行约定
├── scripts/                  # 统一入口脚本（后续实现）
├── src/rose_xmd/
│   ├── cli/                  # train/eval/preprocess/infer 命令
│   ├── core/                 # 不依赖具体平台的协议与配置
│   ├── data/                 # trajectory、MAP、mask、normalization、dataset
│   ├── models/               # diffusion/inpainting/RePaint 与 encoder
│   ├── progress/             # progress estimator、window、STPM adapter
│   ├── envs/                 # ManiSkill、LIBERO、Franka 环境适配器
│   ├── runtimes/             # trainer、rollout、evaluator、inference
│   └── integrations/         # 第三方包导入与平台 glue code
├── tests/                    # unit、contract、integration
└── third_party/              # 外部仓库路径/版本说明
```

## 外部源码

默认外部源码路径由环境变量指定，详见 `third_party/*/README.md`：

```bash
export ROSE_MANISKILL_ROOT=/home/hebu/code/mam/ManiSkill
export ROSE_MASKED_ACTION_ROOT=/home/hebu/code/mam/Masked-Action-Model
export ROSE_LEROBOT_ROOT=/home/hebu/code/mam/lerobot_mam
```

## 当前状态

- 已完成统一目录与模块边界设计。
- 未迁移旧代码。
- 未改变旧仓库的工作区状态。
- 下一步按确认后的边界逐模块迁移，并为每个平台保留最小可运行 smoke test。

详细说明见：

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/code_map.md`](docs/code_map.md)
- [`docs/migration_plan.md`](docs/migration_plan.md)
