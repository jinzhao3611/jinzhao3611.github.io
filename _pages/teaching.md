---
layout: archive
title: Teaching
author_profile: true
permalink: /teaching/
classes: wide
---

## Course Materials

### COSI-231A: Statistical Approaches to Natural Language Processing
**Brandeis University, Fall 2024**

I designed programming assignments for this graduate-level NLP course. Below is a sample assignment where students implement core Transformer components from scratch.

---

## Programming Assignment: Transformer Encoder for Discourse Relation Classification

**Course:** COSI-231A Statistical Approaches to Natural Language Processing
**Term:** Fall 2024
**Due Date:** November 26, 2024
**Points:** 100

---

## Overview

In this assignment, you will implement a **simplified Transformer encoder** from scratch and apply it to **discourse relation classification** using the Penn Discourse Treebank (PDTB) dataset. By completing this assignment, you will gain hands-on experience with the core components of the Transformer architecture, including:

- **Sinusoidal positional embeddings** for encoding sequential information
- **Multi-head self-attention** mechanism
- **Feedforward neural networks** within the Transformer block

Understanding these fundamental building blocks is essential for working with modern NLP models such as BERT, GPT, and their variants.

---

## Learning Objectives

Upon successful completion of this assignment, students will be able to:

1. Explain the role of positional embeddings in Transformer architectures and implement sinusoidal positional encoding
2. Implement the scaled dot-product attention mechanism and extend it to multi-head attention
3. Build a complete Transformer encoder block and apply it to a text classification task
4. Analyze the impact of architectural choices (e.g., number of attention heads, positional embeddings) on model performance
5. Conduct systematic experiments and report findings in a clear, scientific manner

---

## Background: Discourse Relation Classification

Discourse relations describe how two text segments (arguments) are logically connected. For example:

| Arg1 | Arg2 | Relation |
|------|------|----------|
| "It was raining heavily" | "We decided to stay home" | Cause-Result |
| "The company profits increased" | "However, employee satisfaction dropped" | Contrast |

The PDTB corpus annotates such relations between adjacent text spans in Wall Street Journal articles. In this assignment, we classify relations at **Level 2** of the PDTB sense hierarchy, which includes categories such as:

- `Comparison.Contrast`
- `Contingency.Cause.Reason`
- `Contingency.Cause.Result`
- `Expansion.Conjunction`
- `Expansion.Instantiation`
- `Temporal.Asynchronous`
- And others...

---

## Dataset

The PDTB dataset is provided in JSON Lines format with train/dev/test splits:

```
data/pdtb/
├── train.json    # Training set
├── dev.json      # Development set (for hyperparameter tuning)
└── test.json     # Test set (for final evaluation)
```

Each line in the JSON files contains a discourse relation with the following fields:

| Field | Description |
|-------|-------------|
| `Arg1` | First argument text span |
| `Arg2` | Second argument text span |
| `Connective` | Discourse connective (may be empty for implicit relations) |
| `Sense` | Discourse relation label(s) |
| `Type` | Relation type (Explicit, Implicit, EntRel, etc.) |

---

## Project Structure

```
PA4_starter_code/
├── README.md                 # This file
├── data/
│   └── pdtb/                 # PDTB dataset
│       ├── train.json
│       ├── dev.json
│       └── test.json
└── starter_src/
    ├── run.py                # Main training script
    ├── model.py              # Model architecture (TO IMPLEMENT)
    └── corpus.py             # Data loading utilities (TO IMPLEMENT)
```

---

## Implementation Tasks (50 points total)

### Task 1: Data Loading (`corpus.py`) — 15 points

Complete the `PDTBDataset` class to create a PyTorch Dataset for the PDTB data.

**Requirements:**
- Implement `__init__()`: Store relations, vocabulary, max length, and label mapping
- Implement `__len__()`: Return the number of samples
- Implement `__getitem__()`:
  - Concatenate Arg1, Arg2, and Connective with special tokens: `[SOS] + Arg1 + [SEP] + Arg2 + [SEP] + Connective + [EOS]`
  - Encode tokens to indices using the provided vocabulary
  - Pad or truncate sequences to `max_len`
  - Return (label_tensor, text_tensor) tuple

### Task 2: Sinusoidal Positional Embedding (`model.py`) — 10 points

Implement the `forward()` method of the `PositionalEmbedding` class.

**Mathematical Formulation:**
```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

**Implementation Steps:**
1. Compute `half_dim = hidden_size // 2`
2. Create frequency decay factors using exponential decay
3. Multiply positions by frequencies to get phase values
4. Apply sine to even dimensions and cosine to odd dimensions
5. Concatenate to form the full positional embedding

### Task 3: Multi-Head Self-Attention (`model.py`) — 15 points

Implement the `forward()` method of the `MultiHeadSelfAttention` class.

**Implementation Steps:**
1. Apply linear transformations to queries, keys, and values
2. Reshape tensors to split the embedding dimension across multiple heads
3. Compute scaled dot-product attention:
   ```
   Attention(Q, K, V) = softmax(QK^T / √d_k) V
   ```
4. Apply the attention mask to prevent attending to padding tokens
5. Compute weighted sum of values using attention weights
6. Concatenate heads and apply final linear projection

**Important:** You must implement this from scratch. Using `torch.nn.MultiheadAttention` is **not allowed**.

### Task 4: Transformer Encoder (`model.py`) — 10 points

Implement the `forward()` method of the `MiniTransformerEncoder` class.

**Implementation Steps:**
1. Embed input tokens using the embedding layer
2. Generate and add positional embeddings
3. Create attention mask for padding tokens (True for real tokens, False for padding)
4. Apply multi-head self-attention
5. Pass through feedforward block
6. Apply final classification layer

---

## Experiments (50 points total)

Experimental analysis is a critical component of this assignment. You must conduct the following experiments, report quantitative results, and provide thoughtful analysis.

### Experiment 1: Baseline Without Positional Embeddings — 15 points

Train the model **without** positional embeddings to establish a baseline.

**Deliverables:**
- Report training curves (loss over epochs)
- Report final accuracy on dev and test sets
- Provide qualitative analysis:
  - Why might position information be important for discourse relation classification?
  - What patterns might the model miss without positional information?
  - Examine specific examples where the model fails

| Metric | Dev Set | Test Set |
|--------|---------|----------|
| Accuracy | ___ % | ___ % |
| Loss | ___ | ___ |

### Experiment 2: With Positional Embeddings — 15 points

Train the model **with** sinusoidal positional embeddings and compare against the baseline.

**Deliverables:**
- Report training curves (overlay with Experiment 1 for comparison)
- Report final accuracy on dev and test sets
- Provide comparative analysis:
  - Quantify the improvement from adding positional embeddings
  - Explain *why* positional embeddings help for this specific task
  - Discuss whether certain discourse relation types benefit more than others
  - Visualize attention patterns if possible

| Metric | Without Pos. Emb. | With Pos. Emb. | Improvement |
|--------|-------------------|----------------|-------------|
| Dev Accuracy | ___ % | ___ % | +___ % |
| Test Accuracy | ___ % | ___ % | +___ % |

### Experiment 3: Varying Number of Attention Heads — 20 points

Investigate how the number of attention heads affects model performance.

**Requirements:**
- Test at least **4 different configurations** (e.g., heads = 1, 2, 4, 8)
- Keep all other hyperparameters constant for fair comparison
- Run each configuration for the same number of epochs

**Deliverables:**
- Table comparing all configurations
- Training curves for each configuration
- Analysis addressing:
  - What is the optimal number of heads for this task?
  - Is there a point of diminishing returns?
  - How does head count affect training speed/stability?
  - Theoretical explanation: What do multiple heads capture that a single head cannot?

| Heads | Parameters | Dev Accuracy | Test Accuracy | Training Time |
|-------|------------|--------------|---------------|---------------|
| 1 | ___ | ___ % | ___ % | ___ min |
| 2 | ___ | ___ % | ___ % | ___ min |
| 4 | ___ | ___ % | ___ % | ___ min |
| 8 | ___ | ___ % | ___ % | ___ min |

### Bonus Experiment (Optional) — Up to 10 extra points

Conduct additional experiments of your choosing. Examples:
- Different learning rate schedules
- Layer normalization placement (pre-norm vs. post-norm)
- Different activation functions
- Attention visualization and interpretation
- Error analysis by discourse relation type
- Comparison with different sequence lengths

---

## Hyperparameters

Default hyperparameters are provided as a starting point:

| Parameter | Default Value |
|-----------|---------------|
| Learning Rate | 1e-4 |
| Epochs | 25-50 |
| Batch Size | 128 |
| Max Sequence Length | 60 |
| Hidden Size | 256 |
| Attention Heads | 2 |
| Sense Level | 2 (second level of PDTB hierarchy) |

You are encouraged to tune these parameters and report your findings.

---

## Submission Requirements

Submit the following files:

1. **Code** (50 points)
   - `corpus.py` — Completed data loading implementation
   - `model.py` — Completed model implementation
   - `run.py` — Training script (modify as needed)
   - All code should be well-commented and runnable

2. **Experimental Report** (50 points)
   - PDF document (4-6 pages recommended) containing:
     - **Implementation Notes** (5 pts): Brief description of your approach and any design decisions
     - **Experiment 1 Results & Analysis** (15 pts): Baseline without positional embeddings
     - **Experiment 2 Results & Analysis** (15 pts): With positional embeddings + comparison
     - **Experiment 3 Results & Analysis** (20 pts): Attention head ablation study
     - **Conclusion** (5 pts): Summary of findings, challenges, and lessons learned
     - **Bonus experiments** (up to 10 extra pts): Additional investigations

---

## Evaluation Criteria

### Code (50 points)

| Component | Points | Criteria |
|-----------|--------|----------|
| `PDTBDataset` class | 15 | Correct implementation of `__init__`, `__len__`, `__getitem__`; proper tokenization and padding |
| `PositionalEmbedding` | 10 | Correct sinusoidal encoding formula; proper tensor shapes |
| `MultiHeadSelfAttention` | 15 | Correct attention computation, scaling, masking, and multi-head split/merge |
| `MiniTransformerEncoder` | 10 | Proper integration of all components; correct forward pass |

### Experiments & Report (50 points)

| Component | Points | Criteria |
|-----------|--------|----------|
| **Experiment 1** | 15 | Complete baseline results; thoughtful analysis of position importance |
| **Experiment 2** | 15 | Clear comparison with baseline; insightful discussion of positional embedding benefits |
| **Experiment 3** | 20 | Thorough ablation with 4+ configurations; quantitative comparison; theoretical justification |
| **Report Quality** | — | Clear writing, professional formatting, reproducible results (embedded in above scores) |

### Bonus (up to 10 extra points)

| Component | Points | Criteria |
|-----------|--------|----------|
| Additional experiments | 5-10 | Novel experiments with meaningful analysis and insights |

---

## Getting Started

### Environment Setup

```bash
# Required packages
pip install torch numpy tqdm
```

### Running the Code

```bash
cd starter_src
# Update data path in run.py
python run.py
```

### Tips for Success

1. **Start early** — Debugging neural network code takes time
2. **Test incrementally** — Verify each component before integrating
3. **Use small batches first** — Debug with batch_size=2 to catch shape errors
4. **Monitor training** — Plot loss curves to diagnose training issues
5. **Read the docstrings** — Detailed guidance is provided in the starter code

---

## Academic Integrity

This is an individual assignment. You may:
- Discuss concepts and approaches with classmates
- Reference PyTorch documentation and tutorials
- Use the provided starter code

You may **not**:
- Share or copy code with/from other students
- Use pre-built Transformer implementations (e.g., HuggingFace)
- Use code from online sources without attribution

---

## Resources

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) — Original Transformer paper
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — Visual explanation
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
