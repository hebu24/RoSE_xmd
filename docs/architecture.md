# 统一架构

## 一、统一数据契约

所有平台都向核心层提供以下对象：

```text
Observation
  images: dict[str, Tensor]
  state: Tensor
  task: str | None

ActionChunk
  values: Tensor[B, H, 7]
  normalized: bool

MAPWindow
  values: Tensor[B, W, 7]
  mask: Tensor[B, W, 7]
  progress: Tensor[B, W]
  valid: Tensor[B, W]

ProgressEstimate
  value: Tensor[B]
  confidence: Tensor[B] | None
```

MAP 中 7 个动作维度固定为 `x, y, z, rx, ry, rz, gripper`。平台若使用不同的状态维度，只在 adapter 内完成映射。

## 二、运行链路

```text
raw demo / LeRobot dataset / real H5
          │
          ▼
   DatasetAdapter
          │  Trajectory + metadata
          ▼
  Normalizer + MaskFactory
          │  ActionChunk + MAP
          ▼
 ProgressEstimator ──► MAPWindowBuilder
          │                    │
          └──────────────┬─────┘
                         ▼
                PolicyBackend
                 ├── train
                 ├── rollout
                 └── inference/RePaint
                         │
                         ▼
              Platform EnvironmentAdapter
```

## 三、模块职责

### `core`

只定义协议和配置，不导入 ManiSkill、LeRobot、机器人 SDK。这里的接口是统一三处代码的边界：`DatasetAdapter`、`EnvironmentAdapter`、`PolicyBackend`、`ProgressEstimator`。

### `data`

负责 trajectory schema、动作与状态归一化、mask 家族（structured/random/no-reference）、MAP 构造、demo split 和窗口采样。数据源差异由 `data/adapters` 处理。

### `models`

提供扩散策略编排。主干可以是 DiT 或 U-Net；MAP encoder、visual encoder、state encoder 都是可插拔组件。训练损失支持 known/unknown 区域加权，推理支持 RePaint。

### `progress`

统一离线 progress 标签和在线 progress 推断。STPM 是一种 backend；未来可以接 SARM 或直接使用 oracle progress，但不改变 MAP/window 接口。

### `envs`

把 ManiSkill、LIBERO 和 Franka 的 reset、observation、action、success、episode 生命周期适配到同一环境协议。真机环境禁止被仿真评估逻辑隐式创建。

### `runtimes`

统一训练、预处理、rollout、control error、checkpoint 和 inference 流程。平台脚本只负责选择配置和 backend。

### `integrations`

集中处理外部包导入、路径注入、版本检查和第三方对象转换，避免在核心模型中散落 `sys.path` 修改。

## 四、配置原则

- `configs/base.yaml` 放跨平台默认值。
- `configs/sim/maniskill.yaml`、`configs/sim/libero.yaml`、`configs/real/franka.yaml` 只放平台差异。
- 数据路径、checkpoint 路径和硬件地址通过环境变量或命令行覆盖，不写入源码。
- 外部源码路径由 `ROSE_*_ROOT` 指定；不存在时启动阶段给出明确错误。

## 五、迁移顺序

1. 先迁移 `core` 数据契约和 mask/window 单元测试。
2. 再迁移 ManiSkill adapter，保持现有 MAM 训练与评估结果。
3. 接入 LeRobot/LIBERO 的 dataset/policy/env adapter。
4. 接入 Franka H5 和真实 inference，最后接入机器人传输层。
5. 三个平台都通过 contract tests 后，再删除旧入口的重复实现。
