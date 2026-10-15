# Franka 外部依赖

默认路径：`/home/hebu/code/mam/Masked-Action-Model/franka_train`，真机 inference 相关路径为同仓库的 `mam-realworld-infer/`。

设置：

```bash
export ROSE_MASKED_ACTION_ROOT=/home/hebu/code/mam/Masked-Action-Model
```

接入范围：Franka H5/UMI 数据、25 维 state、robust normalization、STPM 和真实机器人传输层。硬件端运行必须由显式 `franka` 配置触发。
