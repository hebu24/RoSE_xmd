# 统一脚本

后续只保留按平台选择配置的薄脚本，例如：

```text
train_maniskill.sh  -> rose-train --config configs/sim/maniskill.yaml
train_libero.sh     -> rose-train --config configs/sim/libero.yaml
train_franka.sh     -> rose-train --config configs/real/franka.yaml
```

训练参数和数据路径不在脚本中复制一套逻辑。
