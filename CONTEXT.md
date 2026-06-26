# Humanoid Locomotion Runtime

这个上下文定义本仓库的项目语言。它只记录领域术语，不记录实现决策、任务计划或临时想法。

读法很简单：下面每个词都是以后讨论时推荐使用的说法，`避免使用` 是容易造成误会的说法。这里不定义实验结果，也不代表某个 run 已经完成。

## 语言

**A800 单机实验路径**:
默认科研执行路径，把一台 A800 服务器视为实验代码、队列任务、日志和摘要的唯一主机。白话说：同一组实验尽量不要拆到多台机器上跑。
_避免使用_: split-server experiment path, ad-hoc dual-server workflow

**本机工作室**:
本地 macOS 工作环境，用于计划、代码审查、文档和本地 ARIS 科研流程。它不是跑正式 GPU 实验的地方。
_避免使用_: local server, company server

**公司实验服务器**:
用于实际实验执行的远程 GPU 服务器，包括 A800 或 5090 机器。实验结果、夜间任务和 GPU smoke 都按这个环境理解。
_避免使用_: local studio, laptop

**夜间 ARIS 任务**:
白天 handoff 后由 ARIS 无人值守执行的任务，通常包括 smoke tests、queued pilots、multi-seed experiments、monitoring 或 result summaries。没有白天明确 handoff，就不应该自动开跑。
_避免使用_: manual run, daytime inspection

**次日验收检查**:
夜间 ARIS 任务结束后的人工检查步骤，用来判断日志、指标和 artifacts 是否有效，能否解锁下一组 run。它不是随便看一眼日志。
_避免使用_: casual log skim, informal check
