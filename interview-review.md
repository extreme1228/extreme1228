# Post-training / AgentRL / CUA 面试题目整理

## 米哈游

### 2026-06-26 米哈游 二面

#### 1. 自我介绍 + 简历介绍

- 自我介绍 + 简单的简历介绍。

#### 2. 第一段 AgentRL 经历：Rollout 与 Train 分离

- 为什么要 Rollout 和 Train 相分离？
- 他们是怎么相分离的？
- 这个和 StreamRL 的设计有什么区别？

#### 3. 异步 staleness

- 异步的 staleness 怎么解决？

#### 4. micro-batch vs mini-batch 的异步粒度

- 为什么没有做到每个 micro-batch-size 过一遍训练框架，而是等到整个 mini-batch-size 才过？
- 为什么没有做到这样更加异步的设计？

#### 5. AgentRL Controller 的独立性

- AgentRL Controller 是否独立于训练框架？
- Controller 接入新环境是否容易？

#### 6. cross-sampling 与 off-policy

- cross-sampling 的策略引入了更多 RL 理论上的 off-policy，你们是怎么看的？

#### 7. APT 介绍

- 介绍一下 APT，每个模块的核心作用是什么？

#### 8. 自动化接 Benchmark

- 你们是怎么实现自动化接 Benchmark 的？
- 模型如果接完了分数不对齐怎么办？
- 如果遇到特别 heavy 的 docker 环境怎么办？

#### 9. 训练自动化优化

- 训练上是怎么做自动化优化的？
- 人能够自动调配资源，模型 / agent 不能，怎么办？

#### 10. 评估模型决策能力

- 如何更好地评估一个模型 design / 决策的能力？

#### 我反问的问题

- 训练的人数规模？
- 资源情况？
- 具体做什么事情？
- base 在哪里？

### 2026-07-02 米哈游 三面（技术）

#### 1. 自我介绍

- 个人自我介绍。

#### 2. ScaleCUA 工作

- 介绍 ScaleCUA 工作。

#### 3. 大模型 vs 小模型训练

- 除了 paper 外，是否做过更大的模型训练？
- 大模型训练和小模型训练有什么不同？
- 这个 Scaling 的过程中，你最大的体验是什么？

#### 4. 新一代 CUA

- 你认为新一代 CUA 会怎么融入人们的生活？
- 你有什么看法 / 见解？
- 你认为 CUA 和 coding 是什么关系？

#### 5. APT 介绍

- 介绍 APT，你们现在的成果有哪些？
- 做这个的过程中个人体会有哪些？

#### 6. APT 的价值

- 你认为 APT 真正帮助了你什么？

#### 7. 长程任务 RL 与 credit assignment

- 如何解决长程任务 RL 中 credit assignment 的问题？
- 为什么智谱又用到了 PPO？
- 之前为什么大家从 GRPO 转到了 PPO？现在为什么又转回了 PPO？
- critic 应该怎么训练才能预测准？

#### 8. domain 模型的训练规划

- 如果你负责一个 domain 的模型，你会如何安排预训练 / 中训练 / 后训练这几部分的权重和流程？
- 什么是重要的，什么是不重要的？
- 哪些数据应该放到 SFT，哪些数据应该放到 RL？

#### 我反问的问题

- 米哈游和 Annapurna / annutacon 的关系？
- 如何理解多模态数据？
- 各家是如何训练原生多模态模型的？
- 为什么 Google 的 Gemini 多模态能力这么好？

## 腾讯青云

### 2026-07-02 腾讯青云 三面（HR 面）

#### 1. 实习

- 是否能实习？

#### 2. 面试进展

- 现在面过几家？

#### 3. 对腾讯的考虑

- 对腾讯怎么考虑？

#### 4. 离职动机

- 为什么要离开智谱？
- 考量是什么？

#### 5. 薪资

- 薪资要求？

### 2026-07-22 腾讯青云 技术面

#### 1. 自我介绍 + 简单项目介绍

- 自我介绍。
- 简单介绍项目经历。

#### 2. 项目一 AgentRL：RL 框架设计

- 介绍你们的 RL 框架是怎么设计的。
- 介绍框架是怎么实现异步 RL 的。
- 为什么要做异步？
- 异步相比同步的优势是什么？

#### 3. AgentRL 过程中的最大问题

- 这个过程中遇到的最大问题是什么？
- 你们是怎么解决这个问题的？

#### 4. 最大训练模型规模

- 最大训练过多少参数规模的模型？

#### 5. 项目二 ScaleCUA 方法细节

- 介绍 ScaleCUA。
- 说明方法细节。

#### 6. 未来 CUA 架构

- 你认为未来的 CUA 会是什么架构设计？

#### 7. GUI 前景与 Coding 结合

- 你认为 GUI 未来是否有前景？
- 怎么看待 coding 和 GUI 相结合？

#### 8. 反问问题

- 反问问题待补充。

## Kimi

### 2026-07-08 Kimi 技术二面

#### 1. 自我介绍 + 项目介绍

- 自我介绍加项目介绍。

#### 2. AgentRL 异步 vs 同步

- AgentRL 中异步相比同步的优势？
- 如何处理 off-policy 的问题？
- Rollout / training 的 GPU 资源怎么分配？
- training 模块参数更新的时候是否会影响 Rollout？

#### 3. Rollout 的 KV cache

- Rollout 的 KV cache 有没有关注过？
- 中间模型参数更新之后是否会导致之前的 KV cache 全都失效？

#### 4. ScaleCUA by-traj 的 compact 删图

- ScaleCUA by-traj 训练进行 compact 删图的方式，和你们提到的 sliding-window 方式很像吗？

#### 5. CUAGym 这篇 paper

- 是否关注过 CUAGym 这篇 paper？
- 怎么看待这篇论文？
- 和你们做的是否有什么区别？

#### 6. 数据生成的多样性

- 数据生成如何确保多样性？

#### 7. Frontier Sampling 的优势与评测

- 体现 Frontier Sampling 的优势，是否应该表现为 training reward 基本维持在 50%、test-set 分数上涨？
- 对比方法是否需要对比 test-set 上的分数？

#### 8. benchmark 的数据构造

- 对于 OSWorld-v2 和 SASS-Bench 这类 benchmark，有什么数据构造的方法？

#### 我反问的问题

- Kimi 对 CUA 是怎么看待的？
