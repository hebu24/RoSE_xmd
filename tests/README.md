# 测试布局

- `unit/`：MAP、mask、normalization、window 等纯函数测试。
- `contract/`：三个平台必须满足的 dataset、environment、policy contract。
- `integration/`：需要外部源码、仿真环境或硬件模拟器的测试。

框架评审阶段只保留目录，不执行平台测试。
