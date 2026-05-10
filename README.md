# AGents-with-Laws
The following examples illustrate different paradigms for integrating legal knowledge into agent-based systems, including structured reasoning pipelines, retrieval-augmented generation, multi-agent collaboration, and latent decision-making frameworks.  
以下示例说明了将法律知识集成到基于代理的系统中的不同范式，包括结构推理流程、检索增强生成、多代理协作和潜在决策框架。

## 1. JurisMMA
This project builds upon the JurisMMA framework and JurisMM dataset introduced in [Multimodal Multi-Agent Empowered Legal Judgment Prediction](https://arxiv.org/abs/2601.12815).  
本项目基于多模态多智能体赋能的法律判断预测中介绍的JurisMMA框架和JurisMM数据集。

## 2. AgentCourt
This project is Simulating Court with Adversarial Evolvable Lawyer Agents introduced in [AgentCourt: Simulating Court with Adversarial Evolvable Lawyer Agents](https://aclanthology.org/2025.findings-acl.304.pdf).


# Experiment and Implementation

## 1. Make a start Intake Agent Module（准入与授权模块的落地与工程实践）
- Target Transform unstructured materials into structured JSON data to generate standardized legal documents (e.g., Power of Attorney).<br>
  将非结构化材料转化为结构化 JSON 数据，并生成标准化法律文书（如《授权委托书》）。
- Evolution Path: Framework Binding -> Resolving "Schrödinger's Bug" -> Architectural Upgrade <br>
  阶段一：框架绑定<br>
  基于 LangChain，利用大模型结构化输出绑定 Pydantic 模型，提取核心实体。<br>

  阶段二：解决“薛定谔的 Bug”<br>
  发现国内大模型 API（因 vLLM 引擎波动或安全拦截）常返回非标 JSON（如 choices: null），导致原框架崩溃。<br>

  阶段三：架构升级<br>
  中间件拦截：构建自定义拦截器，裸调底层网络请求，暴力提取文本后再用 JsonOutputParser 解析，大幅提升鲁棒性。

## Reference

```bibtex
@inproceedings{kang2026multimodal,  
  title={Multimodal Multi-Agent Empowered Legal Judgment Prediction},  
  author={Kang, Zhaolu and Gong, Junhao and Chen, Qingxi and Zhang, Hao and Liu, Jiaxin and Fu, Rong and Feng,Zhiyuan and Wang, Yuan and Fong, Simon and Zhou, Kaiyue},  
  booktitle={ICASSP 2026 - 2026 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},  
  year={2026},  
  organization={IEEE}  
}

@inproceedings{chen2025agentcourt,
  title={Agentcourt: Simulating court with adversarial evolvable lawyer agents},
  author={Chen, Guhong and Fan, Liyang and Gong, Zihan and Xie, Nan and Li, Zixuan and Liu, Ziqiang and Li, Chengming and Qu, Qiang and Alinejad-Rokny, Hamid and Ni, Shiwen and others},
  booktitle={Findings of the Association for Computational Linguistics: ACL 2025},
  pages={5850--5865},
  year={2025}
}


