# Cascade: A Sub-5ms Predictive Routing Architecture for Large Language Models

## Abstract

Enterprises currently face a severe resource misallocation in AI inference. Due to the stochastic nature of Large Language Models (LLMs), engineering teams default to utilizing expensive frontier models (e.g., GPT-4o, Claude 3.5 Sonnet) for all interactions, regardless of complexity. This whitepaper introduces Cascade, an intelligent, localized C++ routing proxy. By executing a highly distilled machine learning classifier ahead of the inference lifecycle, Cascade predicts prompt complexity in under 5 milliseconds and routes traffic to the most cost-effective model, achieving up to 75% cost reduction with zero degradation in end-user application latency.

## 1. The Latency-Cost Tradeoff in AI Routing

The premise of dynamic model routing is economically sound: route simple tasks to cheap models and complex reasoning tasks to frontier models. However, the current implementations of AI proxies introduce fatal architectural flaws.

If an AI proxy saves $0.001 on a prompt but introduces 150ms of network latency, the economic benefit is nullified by the destruction of the real-time user experience. We benchmarked Cascade against the current State of the Art (SOTA) routing methodologies:

| Architecture | Implementation Details | Latency Overhead | Scaling Bottleneck |
|---|---|---|---|
| **Cascade Router** | Bare-Metal C++, INT8 ONNX, SIMD JSON | **~4.6 ms** | Negligible (Lock-free arenas) |
| Python Proxy | LiteLLM, FastAPI, Uvicorn | ~65.0 ms | Python GIL, Garbage Collection |
| SaaS Router | Third-party managed proxy | ~180.0 ms | External Network TLS Handshake |
| LLM-as-a-Judge | Using an LLM to route prompts | ~850.0 ms | Time-To-First-Token (TTFT) |

![Latency Comparison](latency_chart.png)

## 2. System Architecture

Cascade abandons brittle, deterministic heuristics in favor of a specialized machine learning classification layer pushed down to the metal.

### 2.1 Feature Extraction Layer

- **Zero-Copy Parsing:** Utilizes simdjson to extract strings without allocating new memory buffers.
- **Truncated Tokenization:** Implements a custom C++ WordPiece tokenizer. To maintain the < 5ms budget, the proxy isolates and tokenizes only the first 16 tokens of the prompt, reducing attention mechanism overhead by nearly 85%.

### 2.2 Local Inference (The "Brain")

The tokens are passed to an INT8-quantized all-MiniLM-L6-v2 embedding model executing within the ONNX Runtime ecosystem. The resulting 384-dimensional semantic vector is fed into a locally trained Logistic Regression model. The output is a calibrated probability distribution: $P(\text{success}\mid\text{model}_i)$.

## 3. Training & Validation Methodology

To train the predictive weights, we constructed an automated "LLM-as-a-Judge" pipeline. On a curated 800+ prompt dataset, the judge determined that the smaller model successfully answered 75.5% of the prompts. Our Logistic Regression classifier, trained on this dataset, achieved a baseline accuracy of 67.8% on hold-out data.

## 4. Progressive Escalation & State Preservation

To eliminate enterprise risk, Cascade implements an optimistic routing cascade. The prompt is routed to the lowest-cost candidate model. If the output fails runtime validation, the proxy intercepts the failure and seamlessly re-routes the original payload to the frontier model within a single HTTP connection.
