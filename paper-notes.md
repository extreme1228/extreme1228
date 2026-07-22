# Paper Notes

> 每日论文阅读与点评,自动从本地笔记同步。

---

## 5.25

- Gym-anything(https://arxiv.org/pdf/2604.06126)

    - 论文提出了一个根据现实场景中的软件自动化接入Benchmark，构建环境镜像、生成任务、生成Verifier的ai自动化流程Gym-anything,并在这套流程上将现实场景中的任务转化为了200+个真实的docker环境并得到了10k+的CUA任务，搭建了CUA-World这样一个Benchmark：

        - 在Scaling环境方面，设计了一个multi-agent system，有负责create环境的agent，负责修改的agent，负责verify的agent，并提出各个agent memory共享机制，使得agent能够实现迭代学习的流程

        - 在Scaling Task方面，有opus或gpt去与真实环境交互得到高质量种子任务，之后用Gemini3-Flash进行扩增。

        - 在Scaling Verifier部分，通过Rubric的方式在生成任务的时候进行规范定义

    - 点评：论文所体现的这样一种自动化Scaling环境的思想值得参考，多Agent 共享memory迭代进化的思想也值得参考但是论文并没有在ai for ai这个自动化流程上展开过多的介绍，可能暂时没有在这方面有比较成熟的经验或者实验结论。

---

## 5.24

- Skill0(https://arxiv.org/pdf/2604.02268)

    - 本质上是一种尝试将推理时使用SKILL通过In Context RL将Skill的内容内化到模型参数内部的一种方法，论文通过随着RL的进行逐渐减少SKILL的使用（中间设计了一种类似课程学习的机制去调控SKILL的依赖程度）使得模型在训练的过程中逐渐学会SKILL中的内容，在alfworld，webshop，search-qa上实现提升的同时，降低了token平均消耗

        点评：

        1. 一方面我不太理解什么场景需要内化SKILL到模型内部，用闭源模型的时候没办法训练，用开源模型的时候训练成本又太多，另一方面本身我们提出SKILL这样一个概念就是为了给LLM添加外部知识库，使得LLM在工作的时候能够动态的根据skill的内容去更准确的实现，将SKILL的能力内化到LLM内部这个出发点虽然好但是现实生活中的场景无穷无尽，我可以很快的外部添加一个skill，但我不可能动态地实时训练一个skill，同时论文也没有证明这个基于SKILL的训练没有对其他场景造成效果的损失。

        2. 再次我实际上没有看出来这个和之前的RAG-RL有什么区别，完全看不到一点收益。

---

## 5.17

- SCALECUA，这篇工作主要是一个data-driven的工作，收集构造了大量CUA场景的数据并做了整理得到了相对还可以的效果。（https://arxiv.org/pdf/2509.15221）

- DeepSeek-V4 技术报告：全篇读完感受只有一个，DeepSeek在训练infra上真可谓是做到了国内顶尖，国内外目前没有任何一家大模型公司开源出来的技术报告有着这么详细的模型架构，训练方法，甚至包括推理优化等细节。总的来说这次DeepSeek-v4的创新点在于：

    - 模型架构上，大体沿用了DeepSeek-v3.2的架构，在网络设计上使用了mHC（流型约束残差连接）的方法在保证多条残差流使得模型表征能力更强的基础上通过约束残差映射矩阵保证数值稳定性。

    - 注意力机制上，为支持1M长上下文，模型结合采用了CSA（compressed Sparse Attention）和HCA（Heavy Compressed Attention）两种注意力相结合的技术：其中CSA技术对于输入的hidden states进行相邻m个entry的压缩处理，之后利用Sparse Attention的设计对query进行indexer处理，将indexer之后的query与Compress的keys进行index score的计算，之后选择top-k个kv entries，同时还有计算sliding-window的kv entries与刚刚计算出来的top-k的kv entries进行contact，最后进行Attention计算； 而HCA则是进行高强度压缩，直接对原始kv entries进行高强度压缩之后做full Attention。

    - 训练上，采用了Muon Optimizer，Muon Optimizer相比于AdamW更关注整个权重矩阵W整体的更新梯度因此更适合大模型训练。

    - 在训练infra上，优化了EP的训练效率低的问题，使用TileLang编写kernel算子，通过deepgeem确保同一个token 在不同batch也要bitwise一致，同时训练上采用FP4 aware training，极大地优化了训练和推理速度

    - 推理上采用了异步kv cache和磁盘kv 复用

    - 后训练方面，采用在特定领域训练（sft + rl）之后通过OPD合并到一个模型中，同时在OPD中采用full vocabulary的逆向KL散度计算，更贴合概率分布，同时在后训练RL infra上也做出了多项优化，包括

        - FP4集成rollout

        - 可抢占式调度及错误容忍性推理服务

        - Million-token rollout 管理，将rollout数据拆解为轻量级的metadata而非整个轨迹

        - Desc沙箱平台支持大量环境接入

---

## 3.26

- NVIDIA-GTC：

    - openclaw的爆火带来的推理拐点，推理资源需求大增

    - nvidia改变策略从卖显卡变为卖token

    - ai五层蛋糕 

        - 能源

        - GPU\\芯片

        - Infra

        - Models

        - Application

---

## 3.25

- DART-GUI（https://arxiv.org/pdf/2509.23866），这篇论文是25年的ICLR，面相的Benchmark也是OSWorld，主要的创新点有：

    - 训推分离，异步架构（和agentrl相似）

    - 预先收集高质量数据来解决困难任务rollout奖励稀疏的问题

    - 动态调整rollout-number和traj-length

    - 训练high-entroy的step

- 但是这篇论文最后采用了在osworld-std-subset上直接训练的方法，可借鉴内容不多。

- ScienceBoard(https://arxiv.org/pdf/2505.19897)

---

## 3.24

- ACuRL（https://arxiv.org/pdf/2602.10356），这篇论文算是Self-Play，RL-Zero在GUI Agent上的尝试，论文同样类似地提出了Task Generator（GPT5驱动），Dynamic Sampler（每个iteration更新任务难度但没说怎么实现），CUA-judge（llm-judge）整体这样的逻辑，但是只选取了OSWorld和OfficeWord以及ScienceBoard中相对简单的任务进行实验，结果其实上涨也一般。思路可以学习，但真正的将GUI Agent从RL from zero还是很难，但是可以参考这篇论文是怎么把ScienceBoard跑起来的

---

## 3.20

- AttnRes ： Kimi Attention的新架构创新，论文的主要思路是将序列层面上的Attention机制旋转90度应用到前向传播的逻辑中，论文指出传统的ResNet在面临网络层数深的情况下可能出现历史信息丢失遗忘，ResNet的本质推导出来其实就是第n层的输出本质是前n-1层的权重相同情况下的求和，但实际上不同的层可能对历史层所需要的权重不一定是相同或者说一致的，故此论文提出可以参考我们对在seq维度上从RNN迁移到Attention的机制，动态引入每一层的权重，计算第n层的输出的时候对前n-1层求一个加权，这里的q矩阵可以新添加一个可学习参数w，v矩阵可以用每层的输出h代替，问题在于如果使用最简单的实现逻辑的话这确实没有什么问题，因为中间层的这些hidden states都是作为激活值存起来的，但是在大规模参数模型训练过程中，为了减少显存压力我们经常会用到PP流水线并行以及recompute等技术：

    - PP流水线的话使用AttnRes会带来较大的通信开销

    - recompute则会导致计算对应权重的时候hiddenstate不存在了，

- 为此论文提出BlockAttnRes的技术，对整个模型架构进行分层，每个Attention加MLP算一层，8个作为一个Block，Block中实行AttnRes计算，层间采用传统Full-Attention机制，解决了PP的问题。

---

## 3.16

- **Training Compute-Optimal Large Language Models （DeepMind Scaling Law）：**这篇论文主要从如何训练一个compute-efficent的大模型做的一个Scaling Law的论文，论文中提出虽然之前的很多论文以及大模型的训练技术报告中都先后提到了Scaling Law，但是大部分仅仅在尝试Scaling Model Size而忽视了训练数据的数量和质量，论文中指出经过大量不同size小模型的消融实验，在给定FLOPS的情况下，Model size和Data Size应该同比例增长，甚至在数据质量高的情况下，小模型也可能训练出更好的效果；同时论文中也详细探讨了FLOPS，Model size和Data Size之间的关系，分析了在给定FLOPS的情况下不同的Model Size对应的最优Data Size.




## 3.12

- GSPO: GSPO这个算法是为了解决grpo算法中天然存在的问题：在Multi-turn和longcontext领域，单次的回复y非常长，这个时候grpo总是利用整个traj的reward结合上per-token的Importance-weight进行优化，不太合理，论文提出在seq-level上进行IS的估计，保证对于整个序列的IS一致，clip-ratio明显升高，训练效率和收敛效率明显上升，同时也提出了GSPO-token的方法，保证可以针对不同token给予不同的adv。

- Jason Wei Some intuitions about LLMs:

    - Next token prediction is actually multi-task learning

    - Scaling llm (compute = model_size * data)

    - Overall accuracy improves smoothly but downstream categories improve fast

---

## 3.8

- 重读DP、TP、SP、CP、PP原理，总结如下：

    - DP：数据并行，将global batch size按照gpu count分为不同的mini batch size不同的卡上训练不同的数据最后通过allreduce计算平均梯度，一般来说默认dp size就是gpu 卡数，随着设置tp、cp等其他参数，一般满足dp * tp * cp = gpu_count

    - TP : tensor parallel，矩阵参数并行，主要是指对MLP和Attention层的权重矩阵进行切分，切分到不同GPU上分别计算最后通过all-reduce或者all-gather操作合并结果（主要取决于是行切分还是列切分，一般会选择通信开销最小的组合）

    - SP：seqence parallel,序列并行，主要为解决长序列情况下activation显存占用大的问题，一般同TP一起使用。通过核心原理：`All-Reduce` = `Reduce-Scatter` + `All-Gather`，将中间计算dropout和layernorm的部分也分为切分后的矩阵执行而非完整矩阵执行。

    - CP：context parallel，上下文并行，针对long context情况下attn计算显存占用n^2开销太大的问题，提出直接将序列按照cp进行切分，每个gpu维护其对应的子Q，K，V矩阵，在计算完sub-attn的结果之后，使用ring-attention的机制，每个GPU的Q矩阵维持不动，按环形依次传递K，V矩阵并计算一共传递CP size次，使用flashattn中的block-wise softmax的逻辑进行增量计算attn结果最后合并。

    - PP：pipline parallel，流水线并行，将模型层数按照GPU进行分块，流水线运行micro batch size，同样的还有单个GPU内部的流水线并行称之为vpp（vritual pipline parallel）

---

## 3.1

- Deepmind 视频：

    - 成立DeepMind提出DQN算法解决Atari Games

    - Google收购获得极大算力提出AlphaGo取得围棋胜利

    - DeepMind创始人Demis小时候国际象棋上有卓越天赋，在一场比赛中他感悟到应该走向AI而非国际象棋职业选手

    - DeepMind开始构建虚拟环境（gym） reward-based rl

    - 提出AlphaStar 开始解决星际争霸

    - Demis 16岁时加入游戏公司构建AI游戏

    - 提出AlphaFold解决蛋白质折叠问题，虽然在CSAP13比赛中取得领先但是团队认为远没有解决这个问题

    - 在CSAP14中团队取得更大的进展，准确率提高至90+，alphafold绝对对全球开放

- DeepSeek V3.2技术报告，主要有两点值得注意的：

    - 提出DSA稀疏注意力机制，相比传统的Full Attention，提出可以对每个token提前计算一个其他token对于他的权重分布，然后计算注意力的时候每个token只计算和他最相关的top-k个token的注意力

    - 而是mask改进的GRPO，主要指的就是对于adv < 0 且IS weight比较大的token的loss进行mask（乘0）处理来防止负adv对整体RL的影响，这部分和BAPO的想法有点类似。

---

## 2.28

- BAPO(https://arxiv.org/pdf/2510.18927) 文章主要通过分析RL训练过程中entropy，token probilitiy, clip ratio等参数提出了一种动态调整clip的上下界，确保训练过程中adv为正的样本在总体的loss中占比大于一个固定的比例（0.4），通过动态调整的方法，可以有效地将DAPO中的clip-higher方法扩展，对于entropy下降，解决off-policy问题有一定的帮助。

- 现代RL系统为了加快训练和推理速度，大多采用async rollout的方法，这种方式会导致IS weights变得极端，相比于严格on-policy的算法更容易触发clip机制，进而导致很多高adv低概率的token被截断，使得模型探索能力下降，entropy下降进而影响整体效果。

- 论文显示的结果最后clip-higher都接近2左右了

---

## 2.20

- GLM5 tech report: 简单总结就是

    - 预训练使用了DeepSeek-V3.2的模型架构与DSA（DeepSeek Sparse Attention）并在GLM5的size和模型架构上做了一些改进

    - SFT蒸馏claude的interleave thinking进行训练

    - RL在slime上进行GRPO + IcePop的训练并最后通过On policy distilation进行合并

---

## 2.14

- MiniMax RL框架forge：blog中首先指出当前RL框架所面临的一些问题：

    - agent扩展性和框架灵活性

    - 系统效率和计算延时

    - 信用分配和优化稳定性

- 针对上述问题，forge框架将整个框架设计为agent层、middware层和engine层

    - agent层分为白盒agent（模型对开发者可见），黑盒agent（特指现在的一些agent框架例如cc，opencode，codex等）

    - middware层负责管理agent层发送过来的信息流并同时传递给engine层，同时还有一个data pool用来管理正在进行的任务和已经完成的任务，维护一个buffer

    - engine层负责rollout和training

- 在RL稳定上同时也做出了一些优化：

    - Window IO，类似滑动窗口，用来管理buffer，保证off-policy不太严重

    - 通过tree cache merge的方法，优化Multi-turn任务中cache的响应率，提高整体吞吐量

    - 采取MTP（一次预测多个token）的方式提高系统效率

---

## 2.4

- 重读On-policy distiliation：其实本质就是sft和RL的一个综合，在actor自己的分布上进行采样，通过KL散度作为损失函数将分布尽量和teacher model的分布对齐，一方面避免了RL 奖励稀疏，并且不用等待整条trace rollout完成就可以训练，同时也避免直接用SFT时actor模型过拟合到teacher model的行为。

- RLAnything(https://www.arxiv.org/pdf/2602.02488):这篇论文提出对于multi-turn且需要reasoning的任务，结合policy、reward和env可以实现更好的RL效果，论文的主题思路是利用reward model对traj进行单步评分并结合最终的output signal对policy进行优化，而通过最终的真实奖励信号来对reward model的单步进行优化，同时实时统计任务的平均正确率，在保证任务不变的情况下调整任务题目的描述难度。最后在osworld和alfworld以及code任务上进行实验。

- 评论：

    - 核心问题没有解决，论文并没有提及train-set中的最后的任务正确与否是怎么来的，大概是人工标注。

    - alfworld貌似RL的分数太低了，按理说不应该这么低的

    - 环境调整基本等价于仅仅是调整了下Instruction的描述，没什么实质作用。

    - 也没有阐述train-set到底怎么来的。

    - 但是这种GUI Multi-turn的任务利用reward model打分确实肯定比一个单一的reward有效，但如何训练出一个完美的reward model是一个核心的问题。

---

## 2.1

- TTT-discover:这篇论文提出的一个想法是，与其通过RL让模型在某个领域实现平均最佳水平不如通过鼓励他探索，让他在某个问题上实现最佳效果，其他功能甚至基础对话功能全部丧失也无所谓，本质上就是训练模型在测试的时候去过拟合某些特定的题目，论文设计的奖励函数是：

$$
\nabla_\theta J_\beta(\theta) = \mathbb{E}_{\substack{s \sim \text{reuse}(\mathcal{H}) \\ a \sim \pi_\theta(\cdot|s)}} \left[ w_{\beta(s)}(a) \nabla_\theta \log \pi_\theta(a \mid s) \right], \quad w_{\beta(s)}(a) = \frac{e^{\beta(s) R(s,a)}}{\mathbb{E}_{\pi_\theta(\cdot|s)}\left[e^{\beta(s) R(s,a)}\right]}
$$

$$
\text{train:} \quad \theta_{i+1} = \theta_i + \eta \nabla_\theta J_{\beta(s_i)}(\theta_i), \quad \text{reuse:} \quad s_i \sim \text{PUCT}(\mathcal{H}_i)
$$

主要设计了以下三点：

- 鼓励entropy的reward，指数型增加reward

- PUCT，启发式的利用过去的state和context

- 推理时优化参数，

- 论文在数学定理证明、kernel编程，算法竞赛等领域实现了巨大的突破

---

## 1.31

- Kimi K2.5官方技术报告出了，和博客上相比多了一些东西，简单总结下：

    - 强调Text和Vision的joint-optimize，论文强调说zero-vision sft的效果比带图sft的效果更好因为这样能够更加激发模型的无图推理能力

        - 感觉只有大模型有效，小模型不带图估计什么都学不到

    - Agent Swarm部分和博客讲的差不多，我感觉核心就是训练了一个调度器，然后通过类似multi-agent的方式实现BoN的效果

    - RL训练上，基本采用了和MiniRL类似的mask方式来解决训推不一致的问题，并强调这个trick对于long-turn resoning很有效

    -

---

## 1.27

- Kimi K2.5 : 这次的技术报告主要从三个角度出发，团队在Kimi-K2的基础模型架构上进行训练实现了更好的效果

    - Reasoning with vision：报告强调加强了模型视觉推理的能力，并展示了根据给定视频或者图片进行coding和reasoning的过程

    - Agent Swarm或者说是PARL 并行RL，通过设置一个可训练参数的顶层调度器负责分解Task为若干个sub-task，每个sub-task由sub-agent执行，sub-agent为冻结参数，，设置reward 为下面形式来鼓励调度器来更多的建立sub-agent执行并行的任务。

$$
R_t = \lambda_{\text{aux}}(e) \cdot \underbrace{r_{\text{parallel}}}_{\text{instantiation reward}} + (1 - \lambda_{\text{aux}}(e)) \cdot \underbrace{(\mathbb{I}[\text{success}] \cdot Q(\tau))}_{\text{task-level outcome}}
$$

    并引入关键步数的概念来评估并行度

$$
\text{CriticalSteps} = \sum_{t=1}^{T} \left( S_{\text{main}}^{(t)} + \max_i S_{\text{sub},i}^{(t)} \right)
$$

极大地提升了综合效果

- 第三个部分则是Offce能力相关，在Kimi内部构建的两个BenchMark AI Office Bench和General Agent Bench上实现突破。

---

## 1.25

- MiniRL：Qwen团队的一篇有关稳定RL训练的文章，论文首先从理论公式角度分析了一下LLM RL下token-level的loss计算本质上是对真正要优化的seq-level级别的loss的一个一阶近似，意思其实就是说从数学上来看，当我们严格on-policy的时候，token-level的loss计算和seq-level的loss计算是严格等价的。

- 之后的部分，论文以MoE模型Qwen3-30B-A3B为base模型进行实验，验证了不同settings下各种RL trick的作用，首先简单提及了对于MoE稳定RL训练的两种方法R2优化（强行使得训练计算log_probs时激活的专家和old模型激活的专家等同）和R3优化（强行使得训练时计算log_probs时激活的专家和推理时激活的专家等同）

    - On-policy RL：

        - MiniRL + 正常的TIS修正训练推理精度误差是最好的，R2，R3优化没必要，同时长度正则化也没必要

        - 但是TIS非常有必要，否则会严重影响训练的稳定进行

    - Off-Policy RL

        - R2和R3优化有必要，但不同情况下作用不同，当异步程度较小时R2优化方法最佳，当异步程度非常大时R3优化效果最佳

- 同时论文还验证了在稳定RL训练的前提下，不同的冷启动方式最终结果相差不大。

---

## 1.21

- IcePop：https://www.emergentmind.com/topics/icepop

- IcePop是在TIS上的进一步优化并在1T参数量的MoE模型上验证了效果，他去除了PPO算法公式中的clip逻辑，转而采用mask的逻辑，比较训练引擎和推理引擎的比例，如果超过了某个范围，直接将该token的gradient设置为0，防止影响训练，总的来说他构造了这样的loss func：


$$
\mathcal{J}_{\text{IcePop}}(\theta) \sim \mathbb{E}_{a \sim \pi_{\text{infer}}} \left[ \mathcal{M}\left( \frac{\pi_{\text{train}}(a; \theta_{\text{old}})}{\pi_{\text{infer}}(a; \theta_{\text{old}})}, \alpha, \beta \right) \cdot \nabla_\theta \log \pi_{\text{train}}(a; \theta) \cdot \hat{A} \cdot r(a) \right]
$$

$$
k_{i,t} = \frac{\pi_{\text{train}}(y_{i,t} \mid \cdots)}{\pi_{\text{infer}}(y_{i,t} \mid \cdots)}, \quad \mathcal{M}(k) = \begin{cases} k, & \text{if } k \in [\alpha, \beta] \\ 0, & \text{otherwise} \end{cases}
$$

---

## 1.21

- TIS：https://fengyao.notion.site/off-policy-rl

- 重读TIS，从本质上为什么会产生训推不一致的情况以及TIS是如何修正的：

    - 相比于传统RL，LLM RL所需要的action space巨大，history（seq_len）巨大，无法像传统RL一样使用同一个模型采样和训练，因为采样耗时巨大，无法承受；于是现有的LLM RL框架采用训练采样分离的架构进行处理，使用vllm / SGLang 作为单独的采样框架（rollout engine）进行推理得到完整的上下文和最终的reward，而使用fsdp /  Megatron训练框架作为单独的训练引擎，负责前向传播计算每个token（每个action）的概率以及对应的梯度；在这个过程中就出现一个问题，虽然使用了同一个模型，但推理引擎为加快推理速度在精度上做出了若干牺牲来提升速度，导致采样的轨迹和训练框架计算出来的概率不一致而由此产生了off-policy的问题，影响训练稳定性和训练效果。

    - TIS提出可以在对应的loss func中乘以对应的 pi_theta(a \| s) / pi_vllm(a \| s) 比例来模拟出真正的分布，同时这个ratio也需要设置一个常数C作为clip ratio，而这样的设置对于所有gradient-based的方法都可以轻松的改动而实现：

        - Reinforce-TIS

$$
\mathbb{E}_{a \sim \pi_{\text{sampler}}(\theta)} \left[ \underbrace{\min\left( \frac{\pi_{\text{learner}}(a, \theta)}{\pi_{\text{sampler}}(a, \theta)}, C \right)}_{\text{truncated importance ratio}} \cdot R(a) \cdot \nabla_\theta \log \pi_{\text{learner}}(a, \theta) \right]
$$

        - PPO-TIS（需要额外注意的是这里对于PPO的ratio修正不能进行消元，因为这会和原本PPO clip的逻辑相悖）

$$
\mathbb{E}_{a \sim \pi_{\text{sampler}}(\theta_{\text{old}})} \left[ \underbrace{\min\left( \frac{\pi_{\text{learner}}(a, \theta_{\text{old}})}{\pi_{\text{sampler}}(a, \theta_{\text{old}})}, C \right)}_{\text{truncated importance ratio}} \cdot \nabla_\theta \min\left( \frac{\pi_{\text{learner}}(a, \theta)}{\pi_{\text{learner}}(a, \theta_{\text{old}})} \hat{A}, \, \text{clip}\left( \frac{\pi_{\text{learner}}(a, \theta)}{\pi_{\text{learner}}(a, \theta_{\text{old}})}, 1 - \epsilon, 1 + \epsilon \right) \hat{A} \right) \right]
$$

    - 同时论文也通过实验证明，推理引擎的精度越低（int8），off-policy现象越严重，TIS修正越有效，同时论文也指出这种情况再MoE架构可能也存在且对于MoE架构模型的RL是一个更大的挑战。

---

## 1.11

- The Path Not Taken: RLVR Provably Learns Off the Principals：这篇论文的主要探究并验证了RLVR过程到底更新了模型参数的哪些地方，结论是，相比于SFT更新的大部分是模型参数中高曲率，主成分的部分，RLVR的过程主要更新的是低曲率且非主成分的模型参数，这主要由三种限制共同构成：

    - KL散度限制了RL每步更新的参数更新幅度

    - Model-Geometry决定了RL更新的目标方向

    - bf16的精度掩盖了很多非主成分的参数更新，所以使得RLVR看起来的参数更新很稀疏。

- 最终大致的结论就是RLVR会很大程度上保留Base模型的几何参数特性，避免更新主成分参数，同时这些结论在不同的模型，不同的RL方法，不同的训练场景上基本保持一致，同时这样的结论也证明了之前一些在SFT上起作用的参数高效微调方法不一定能在RL上也发挥作用，因为很多PEFT的方法都倾向于直接对主成分进行更新，而这正是RLVR所避免更新的地方，很容易造成模型collpase，同时给出了未来可能在RLVR领域进行PEFT的可行办法，冻结主成分而微调非主成分部分的参数。

---

## 1.3

- PEFT-FOR-RLVR ： 这篇论文研究了之前的一些PEFT方法例如Lora，DoRA，MiSS等在RLVR上各自的表现得出的结论是传统的LoRa并不特别适合RLVR的训练，相比Full-Training效果有所下降，而DoRA等算法反而效果显著，SVD 初始化策略在RLVR中会发生策略崩溃现象，效果出现显著降低，同时RLVR存在表达能力下限，极端的压缩参数更新的大小可能会导致效果剧烈下降

    - 从结果来看，其实LoRA什么的相差不多，论文也最多试验到7B的模型，不一定具备很高的参考价值，但是SVD初始化导致效果剧烈下降这些现象应该是可以作为参考，也可以进一步思考下RLVR到底在更新模型的哪些内容。

---


# 2025

## 12.22

- DFT : 这篇论文提出一种Dynamic-SFT的思想，通过将SFT的公式重写成RL的样子，指出传统的SFT引入了一个有偏的term，会导致模型对于那种比较难的问题的时候会增大梯度倾向于死记硬背那些答案从而导致过拟合不利于模型整体性能，论文通过在token-level的层面引入这个term的纠正来解决了这个问题。

    - 实验验证下来没什么大用，反而可能相比SFT效果变差了不少

---


## 12.8

- AutoIF : 这篇论文是iclr 2025的一篇有关自动生成数据的一篇论文，和当前AutoGen的主题基本类似，就是数据稍微简单，环境稍微简单，绘图方式和写作技巧以及这种以数据生成为论文核心卖点但是又有训练来验证的论文应该如何组织写作。

---

## 12.7

- Absolute Zero ： 这篇论文是Self-Play RL相关的一篇论文，论文的核心目标也是解决当前不管是SFT或是RL都大规模依赖于人工标注或是蒸馏数据的瓶颈，提出通过让模型自己提出任务，自己解决任务的这样一种循环来拜托数据需求，自我持续提升。论文设计的环境是code环境，通过让模型生成代码，输入、输出三者的其中两个预测剩下那个作为RL的任务，python解释器用来判断任务是否执行准确，通过两部分reward：提出题目质量好坏的reward，模型是否作对问题的reward来综合控制模型的训练，最终训练出来的模型在OOD的数学和代码bench上相比base和其他zero-training算法都有明显提升，证明了这项工作的未来前景。

- 读下来感觉想法思路设计很不错，但不管是涉及的任务或是环境都暂时还属于比较简单的类型，本质上其实是通过让模型不断总结自身reasoning的过程，优化reasoning的逻辑从而实现代码和数学能力上的提升，但这一方面受限于模型自身的水平，模型自身水平本身限制了可能无法生成很难的问题和对应的解答，那这部分的能力就永远锻炼不了。还有就是任务类型，生成代码加验证代码本质上都属于比较轻量级的环境比较好验证，但如果涉及到GUI场景，web search、computer use之类的，这些场景下的self-play的任务又该如何定义，值得深思，但论文尝试解决数据来源的思路一定是未来的一个方向，未来的ai如果要在某个领域超越人类就不可能一直局限于人类所设计的问题。

---

## 12.2

- deepseek-v3.2 : 算法上的创新，使用DSA attention机制（没太看懂），在GRPO上的改进

    - 对KL加入IIS优化

    - 对优势加入Mask约束，对于adv < 0 且KL大于一个设定值的seq不计算其adv的loss

---

## 11.28

- Qwen3VL : 主要是一些技术报告的细节，没有太多有价值的东西，只不过qwen系列的训练Pipline似乎已经固化为了三阶段训练 SFT ，Strong to Weak Distillzation RL，还是得结合Qwen3 report看一下 Distillizaiton

---

## 11.5

- AUTOTOOL: AUTOMATIC SCALING OF TOOL-USE CA PABILITIES IN RL VIA DECOUPLED ENTROPY CONSTRAINTS ：这篇论文从LLM + Tool在RL训练中会随着训练的进行出现response变短的现象，从而导致模型无法在困难的问题中有足够的空间去进行resoning，论文针对这一问题，提出了动态调控entropy的loss function，根据问题难度、轨迹长度等动态调控entropy的控制从而使得模型在提高推理能力的前提下实现了在几个tool use数据集上的性能提升。

---

## 11.3

- Game-Tars : 字节推出的通用游戏模型，论文主要强调的点是该模型训练过程中使用了general的action space，基本和人类的操作对齐，论文还提出，游戏数据相比于传统的GUI任务数据，因为大部分时间内当前操作可能和前几秒的操作都完全一致（例如长时间按w控制任务前行），这就导致整个过程不太符合MDP的定义和规范，同时也会导致不是每一步都需要Thinking，论文由此提出sparse thinking的数据构造方法并通过一些tricks构造这些数据，训练模型方面主要用了Pre-training和ICL方法，并没有采用RL算法。

---

## 11.2

- GKD : 这篇文章应该是第一次提出 On-policy Distillation这类方法的，论文提出这种方法基于原先的一些KD的方法的不足，大部分方法都基于expert label data，这与student model的分布很不相似，容易导致模型在训练和推理时见到的数据分布相差过大进而导致效果变差，于是论文提出可以通过on-policy地采样student model自己的数据分布，并让Teacher model基于student的前面的tokens来生成对应的下一个token的logits并最小化他与student预测的logits的KL散度，这样一来，模型训练的时候总是基于自身的分布不断地进行优化，训练也显得更加自然一点，同时论文还指出GKD的这种损失函数设计不仅可以接入利用expert data进行微调的loss fucntion中，也可以接入RL的损失函数中，通过超参数来控制比例。

$$
L_{\text{GKD}}(\theta) := (1 - \lambda) \, \mathbb{E}_{(x,y) \sim (X,Y)} \left[ \mathcal{D}(p_T \,\|\, p_S^\theta)(y \mid x) \right] + \lambda \, \mathbb{E}_{x \sim X} \left[ \mathbb{E}_{y \sim p_S(\cdot|x)} \left[ \mathcal{D}(p_T \,\|\, p_S^\theta)(y \mid x) \right] \right]
$$

$$
\mathbb{E}_{x \sim X} \Big[ (1 - \alpha) \underbrace{\mathbb{E}_{y \sim p_S^\theta(\cdot|x)} [r(y)]}_{\text{RL objective}} - \alpha \underbrace{\mathbb{E}_{y \sim p_S(\cdot|x)} \left[ \mathcal{D}(p_T \,\|\, p_S^\theta)(y \mid x) \right]}_{\text{Generalized On-Policy Distillation}} \Big]
$$

-

---

## 10.29

- On-policy Distillation:这个方法在Qwen3技术报告、Thinking Machine技术报告和GKD论文中都先后有提到，本质上这种方法可以看做SFT和RL的一个折中，SFT属于off-policy，RL奖励太稀疏，于是该方法选择on-policy地采样数据得到输出，并最小化输出和Teacher Model的输出的逆向KL，本质上是将actor model的表现尽量贴近Teacher Model，属于on-policy，又同时对每个token做了奖励信号，有着dense reward。本质上属于soft-RL，方法上类似于PRM对多轮任务中每步给予不同的reward信号。

---

## 10.22

- GLM4.1-4.5V Tech report:这篇论文是GLMV系列的最新技术报告，主要讲述了GLMV系列的模型架构，训练方法和训练架构，其中涉及了数据构造的方法，SFT、RL各个过程中所遇到的一些问题和解决方案，比较让我感兴趣的是这里面的RL过程中引入了RLCS的训练过程即动态调整Rollout过程中数据的难度来保证时时刻刻训练的数据都是中等难度的数据，类似课程学习的思想。

---

## 9.24

- Scaling Agents via Continual Pre-training：这是Tongyi DeepResearch中具体的一篇工作，主要提出了Agent CPT的训练架构，文章花费了比较多的篇幅来描述他构造数据的过程，但主要是在讲有关DeepResearch的数据构造而非通用的数据构造过程，他们提出了一阶动作合成和高阶动作合成数据的相关过程，感觉主要是为了造出更通用，更高质量的sft轨迹数据。

---

## 9.18

- Tongyi DeepResearch: A New Era of Open-Source AI Researchers：这篇blog主要讲了Tongyi团队最近在Web DeepResearch上取得的进展和对应的方法，他们提出了一种新的Agentic 模型的训练范式：CPT(持续预训练) -> (SFT)  -> (RL)整个这样的过程其中SFT和RL方法上没有什么明显的创新点，但是blog中提到他们开发了一个全自动的数据生成系统，能够生成高质量、高难度的WebSearch 问题答案对，质量甚至超过直接在Brosecamp测试集上训练的效果，blog中并没有提及太多的数据生成的细节，貌似是首先对他们收集的web数据进行搭建了一个知识图谱，然后每次随机抽取子表和子图来构建问题答案对，之后类似Agent-evolving的方法，让Agent参与问题的构建并在迭代中提高问题难度与质量。

---

## 9.17

- How Instruction and Reasoning Data shape Post-Training: Data Quality through the Lens of Layer-wise Gradients:这篇文章从具体实验的角度来分析LLM 后训练阶段数据质量到底对模型训练带来了什么样的影响，论文提出了一种全新的评价数据质量的指标——有效秩，来评估数据对模型训练过程中带来的真正影响，高质量数据一般对应着更高的有效秩，论文还通过大量不同参数量不同系列模型的实验证明：

    - 同系列模型下，数据对模型的影响十分相似，同时模型参数量越大，对数据质量的要求越高，能从高质量数据中收获到更多信息但同时也会被低质量数据影响变大。

    - 不同系列模型数据带来的影响差异特别大，但一个基本的原则是数据质量越高（有效秩越大）训练效果越好。

---

## 9.11

- AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning：这篇论文是AgentGym工作的后续，和我们的AgentRL很类似，都是尝试在之前Benchmark搭建的环境上做RL，论文主要强调了其实现了Multi-turn的AgentRL训练和环境框架，在Method方面论文指出过长的turn会使得模型陷入重复无意义的思考而过短的turn则会使得模型的探索空间收到限制，于是论文设置了一个动态增大的turn的超参数，随着训练的进行不断增加从rollout轨迹中选取更新参数的轨迹turn的上限，实现了动态学习的过程，论文分别在AgentGym上的5个单独环境上训练取得了不错的成果（额外添加了DeepResearch环境）

---

## 9.9

- AReal：这篇论文讲述了LLM RL异步训练框架AReal的搭建过程，论文首先指出传统的LLM RL训练更新过程中，因为不同sample数据rollout的长度和时间不一致，同步的更新方法会导致rollout worker\&#34;短等长\&#34;的情况从而导致推理资源的浪费，降低训练效率，论文提出可以将训练更新网络参数的过程和样本采样的过程解耦，在固定的时间同时进行training，参数更新，rollout worker中间不间断，极大地提高了运行速度。但产生了两个问题：

    - 数据陈旧：因为网络参数更新时间和rollout不相关，所以有可能同一个rollout worker中积累了多个不同版本policy的数据 -> 设置超参数限制同一个rollout worker中的数据版本差不能超过固定值

    - 采样打断：因为采样过程中间会遇到policy更新，所以对于同一条轨迹可能前后有多个不同版本的policy参加，从而违背了PPO loss func的本来原理  -> 引入proximal policy 这样的一个假设target更新网络来调整loss func

---

## 9.7

- ON-POLICY RL MEETS OFF-POLICY EXPERTS: HARMONIZING  SUPERVISED FINE-TUNING AND REINFORCEMENT LEARNING  VIA DYNAMIC WEIGHTING:这篇论文主要提出了一种将SFT和RL两个阶段的训练过程合二为一的算法框架CHORD，论文提出，当前LLM大部分的训练范式是两阶段SFT + RL，但是SFT的度很难把控，SFT太少，模型完全没有学会expert data的分布，SFT太多，模型容易过拟合，失去泛化能力，所以本文提出将SFT loss和RL loss合二为一，通过一个参数μ来控制并且这个μ动态变化从接近1变为接近0，使得SFT变到RL的过程没有那么生硬，同时论文还提出在SFTloss上加入token-wise的权重， 对于某个token生成的概率p,权重为p * (1-p)，以此来实现不鼓励太低概率的token来防止中断，不鼓励太高概率的token防止熵崩塌。

$$
\mathcal{L}_{\text{Hybrid}}(\theta) = (1 - \mu) \mathcal{L}_{\text{GRPO}}(\theta) + \mu \mathcal{L}_{\text{SFT}}(\theta)
$$

$$
\mathcal{L}_{\text{SFT-}\phi}(\theta) = -\mathbb{E}_{(x, y^*) \sim \mathcal{D}_{\text{SFT}}} \left[ \sum_{t=1}^{|y^*|} \phi(y_t^*; \pi_\theta) \cdot \log \pi_\theta(y_t^* \mid x, y_{<t}^*) \right]
$$

---

## 9.6

- UI-Tars2(下半)：论文下半部分主要再讲模型Multi-turn RL的训练的一些细节和实验中的一些分析与观察，RL训练同样也是采用的full async模式的Multi-turn RL提高了训练效率，论文将训练任务主要分为GUI-Browsing（搜索）、GUI-General（操作）、GamePlay三大类并分别针对这三类任务使用了一些数据制造手段，论文算法上主要还是采用了PPO算法并应用了诸多有关GAE的算法改进（貌似是为了改进长尾问题GAE估计不准的问题），reward方面，可以被确定正确与否的任务使用二分类reward，其余使用LLM-as-judge的方法，训练Reward Model来评分。

- 比较有意思的是最后提出来的Model Merge的手段，论文提出与其在一个checkpoint上在多个不同任务上连续RL，不如分别RL得到各自领域表现比较好的模型之后直接加权平均他们的模型参数，并证明能实现比较好的效果

$$
\theta^{(\text{merge})} = \sum_{k \in \{\text{GUI-Browsing, GUI-General, Game, GUI-SDK, \ldots}\}} \alpha_k \cdot \theta^{(k)}, \quad \text{s.t.} \quad \sum_k \alpha_k = 1, \; \alpha_k \geq 0 \tag{5}
$$

---

## 9.5

- UITars-2-Report(上半): UITars-2 模型的训练主要是针对GUI Agent场景下的一些任务进行大规模Multi-turn RL训练所得到的一个新模型，在OSWorld、Anroid World和一些Tool-Based Games任务上取得了不错的结果，这篇论文主要介绍了整个模型在搭建过程中所用到的一些核心技术，从数据自动化构造新范式（CT、SFT、RL结合提高数据利用率，RFT成功数据给SFT、失败数据给CT），可扩展型大规模Environment后端支持，多环境RL训练，混合GUI测试环境等等。

- 相较于传统的Multi-turn交互只使用轨迹，这里额外引入了LLM Memory的概念，提升模型上下文理解能力，并将其作为一部分信息传入每一轮的交互信息中

- 方法的前半部分主要都在讲数据构造和环境框架的设计，有点没太看懂2.4.2节的在线交互标注数据流程到底是什么东西？

---

## 9.1

- Pass@k Training for Adaptively Balancing Exploration and Exploitation of Large Reasoning Models：这篇论文主要提出在训练时将pass@1的奖励作为优势值计算梯度改为利用pass@k的奖励作为优势值计算梯度来更新参数，论文通过数学分析提出一种解析解，在得到每轮rollout的结果之后，可以瞬间计算出正例样本所对应的组优势值和负例样本所对应的组优势值从而计算梯度，论文还指出，使用这种方法来更新网络可以让模型更多的关注于提高那些比较困难的样本而非中等难度的样本，同时论文还指出通过两阶段训练 pass@k 加 pass@1 训练能够使得模型在pass@k上的能力迁移到pass@1上，同时论文在末尾还指出了一个未来的探索方向，即完全隐式的奖励函数，可以动态调控模型的表现性能。

    - 值得细看一下，感觉可能对Spider2上的RL训练有所帮助。

---

## 8.31

- LongCat-Flash Report:这是美团最新推出的MoE模型架构的技术报告，目前还没看完，该技术报告主要讲述了LongCat-Flash这个560B MoE架构模型的一些算法创新和训练细节，其中主要的几个贡献有：zero-computation-experts and short-cut-connected MoE(还没完全懂)、多阶段pipline混合训练使得模型各方面能力增强

---

## 8.20

- FlashAttention ：这篇论文介绍了一种优化Transformer 架构模型训练过程中Self-Attention计算的方法，论文从IO角度出发，对Attention计算的QKV矩阵分别进行分块，外层循环K，V，内层循环Q,O 通过单独计算分块后矩阵的Attention值，同时加入Softmax的分块计算方法，实现了Attention计算过程中对HBM访问次数的减少，虽然最终计算FLOPS略有增加，但内存使用和运算速度上都实现了较大提升。

---

## 8.18

- Lora : 这篇经典peft方法的论文介绍了一种高效微调方法，来解决LLM微调时参数量大，消耗资源巨大的问题，论文通过假设预训练好的模型应用在下游任务的过程中所需要调整的参数的内在矩阵的秩是非常小的，提出可以在Self-attention层对Q,K,V,O四个矩阵进行参数更新，更新过程中，原始矩阵参数被冻结，加入两个低秩矩阵来对forward和backward过程进行改进，更新过程也只更新这两个低秩矩阵，实验证明Lora可以在显著减小内存使用和保持推理效率的前提下实现与Full SFT类似的效果。论文在后面的分析中也进一步指出，低秩矩阵的秩不需要特别大，甚至r=1都能够实现不错的效果。

$$
h = W_0 x + \Delta W x = W_0 x + BAx
$$

---

## 8.6

- Your Efficient RL Framework Secretly Brings You Off-Policy RL Training 这篇技术报告中指出目前使用比较广泛的RL框架例如verl，为了减轻rollout阶段的消耗，采用vllm进行rollout而fsdp进行training但是这样会导致即使vllm和fsdp加载了相同的模型参数因为内部结构的不同，对于token的预测也是不一样的，这样会导致online learning变为offline learning，作者提出可以在更新梯度的时候加入一个比例参数来均衡上述的误差累积。

$$
\mathbb{E}_{a \sim \pi_{\text{vllm}}(\theta)} \left[ \underbrace{\min\left( \frac{\pi_{\text{fsdp}}(a, \theta)}{\pi_{\text{vllm}}(a, \theta)}, C \right)}_{\text{truncated importance ratio}} \cdot R(a) \cdot \nabla_\theta \log \pi_{\text{fsdp}}(a, \theta) \right]
$$

---

## 7.31

- GSPO论文阅读：GSPO这篇论文也是对GRPO算法的改进，论文中提出GRPO算法设计存在一个致命的缺陷，它的重要性采样阶段是针对每个token去估计的，这会带来很大的误差，对于long-context的任务尤其明显，甚至会导致模型彻底失效。针对这一问题，GSPO尝试按照seq-level去进行重要性采样，按照sequence-likelihood进行估计解决了GRPO中的这个问题，同时实验结果也指出，这样的改进使得MoE架构的模型训练起来更加稳定。

---

## 7.17

- 完整阅读了一遍skywork的技术报告，整个技术报告中指出了一些对sft后模型RL训练效率以及测试分数可能有帮助的方法并做了丰富了消融实验

    - 数据角度，主要是对搜集到的数据集进行筛选，剔除有错、无关的数据，另外剔除了base模型rollout过程中全对或全错的一些数据

    - 多阶段RL训练，这里的多阶段主要指的是前期max_length 8k后来变成16k再保证最终结果的前提下提高了训练效率

    - 指出对rollout过程中截断的数据的优势值做mask并没有对最终的test score产生影响

    - 指出采样温度是决定模型最终性能的关键要素，所以rollout起始温度一定要高一点

    - 提出了动态控制熵的算法，指出防止RL过程前期熵衰变是使得RL过程最终取得最高分数的关键

    - KL Loss没有作用甚至有副作用

---

## 7.15

- 最近在阅读skywork open-Reasoner1的技术报告，整个技术报告从数据、训练、评测、实验分析等多个角度分析了在sft后的模型上做RL所需要注意的一些地方，从GRPO出发，那些地方可能对RL训练方式熵减的太快，提高测试分数有所帮助，目前看来是一篇不错的技术报告，正在继续阅读

---

## 7.8

- Reject Sampling Fine Tuning一文中对模型在Math上的推理能力进行探索，首先做了一些实验证明了SFT方法下模型的性能提升和数据量的提升成log关系，模型预训练的越好，初始参数量越大，SFT效果越微弱；同时提出RFT拒绝采样方法，先对SFT后的模型进行K采样，经过答案过滤和多样性过滤后构成新的推理路径数据集，在base模型上训练效果优于常规的SFT训练，

---

## 7.7

- Beyond the 80/20 Rule这篇论文是对RLVR这一类算法为什么有用的一篇分析报告，论文从token entropy出发，分析了诸如CoT、RLVR这些方法之所以能够使得模型性能变好，本质上都是模型中20%左右的high entropy token发挥的作用，论文通过Qwen一系列模型，使用DAPO方法，测试了更新 top 20的entropy token和全部更新token来进行对比，发现只更新这些high entropy token反而能够使得模型在AIME上的表现更好，指出了RLVR中核心的原因在于这些high entropy minority token的作用

---

## 6.30

- RLOO这篇文章更像是一个总结性质的论文，他对LLM RLHF时代的方法包括PPO、DPO、RAFT等做了总结并详细介绍了每种方法的公式具体原理及其演变过程，最终提出，LLM时代的RL方法中不必完全照搬PPO中的setting，可以只保留有用的部分，提出RLOO算法，极大的优化了LLM RL训练的成本。

---

## 6.27

- VinePPO这篇论文是对PPO应用在LLM 上出现的CA（信用分配问题）的改进，他没有用PPO这样的直接通过value network来估计每个状态的优势（很不准），也没有像GRPO一样对一条轨迹中的每个状态（token）基于相同的优势估计，而是对每个中间状态进行重新sample，计算MC return来估计每个状态的优势值，在Math和GSM8k上取得了较好的效果

---

## 6.25

- DAPO这篇论文是对GRPO算法的改进，论文尝试通过clip-higher、dynamic-sample、reward-shapiing、token-level loss的几个trick，在Qwen32B上训练，在AIME数据集上超过了单独GRPO的效果（50），也超过了DeepSeek-r1-qwen-32b的效果（47），这篇论文的主要作用是详细分析了RL训练过程中的一些问题和小技巧，如果通过调整一些超参数使得训练变得更加稳定。

---

## 6.24

- GiGPO这篇论文是对GRPO类算法的改进，通过将episode-level的优势估计和step-level的优势估计相结合，旨在解决Agent Multi-turn视角下的信用分配、奖励稀疏等问题；其中step-level的估计过程中将rollout过程中所有出现过的状态s作为一个等价类，在等价类的集合中计算平均优势，最后和轨迹级别的优势估计相结合，在Alfworld（90）和Webshop上实现突破（86/75）

---

