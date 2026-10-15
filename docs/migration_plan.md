# 迁移计划

## Phase 0：当前提交

- 建立统一目录、配置、外部源码说明和接口边界。
- 不移动、不覆盖、不删除旧仓库文件。
- 不引入训练数据、checkpoint、视频和密码。

## Phase 1：核心契约

- 实现 `Trajectory`、`MAPWindow`、`ActionChunk`、`Observation`。
- 实现 mask factory、normalizer、window builder。
- 为 shape、progress 范围、mask 语义添加 unit/contract tests。

## Phase 2：ManiSkill

- 先接现有 H5/JSON 数据和 `pd_ee_pose` 环境。
- 对齐 baseline、MAM、control error、RePaint 四类入口。
- 用旧脚本的固定 seed 和 reset metadata 做回归验证。

## Phase 3：LIBERO

- 接入 LeRobotDataset 与 LIBERO env adapter。
- 保留两阶段训练：random mask，再 structured joint training。
- 加入 Mix0 unseen mask 的评估契约。

## Phase 4：Franka

- 接入 H5/UMI 数据格式、25 维 state 和 robust normalization。
- 接入 STPM progress 与 offline chunk validation。
- 最后接入真实机器人 inference；仿真 evaluator 不得依赖硬件 SDK。

## Phase 5：清理与发布

- 每个平台保留一个统一入口和一个最小配置。
- 删除仅用于历史实验的重复 launcher，保留迁移说明。
- 只有回归测试通过后才迁移下一平台。
