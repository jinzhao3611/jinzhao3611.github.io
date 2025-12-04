#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jin Zhao
# Date: 11/06/24 17:08
"""
Feel free to change/restructure the code below
"""


import torch
import torch.nn as nn

class PositionalEmbedding(nn.Module):
    def __init__(self, hidden_size, device):
        super().__init__()
        self.dim = hidden_size
        self.device = device  # Store the device

    def forward(self, x):
        """
        Implement the forward pass to generate sinusoidal positional embeddings.

        Args:
            x (torch.Tensor): Tensor of shape (batch_size, seq_length) representing
                              input positions or indices.

        Returns:
            torch.Tensor: Tensor of shape (batch_size, seq_length, hidden_size)
                          containing the sinusoidal positional embeddings.
        """
        # Step 1: Compute half the dimension size
        # ----------------------------------------------------
        # Calculate the "half_dim" by dividing self.dim by 2.
        # This will be used to split the sinusoidal and cosine components.

        # Step 2: Create the frequency multipliers
        # ----------------------------------------------------
        # Compute the exponential decay factor to determine how the frequencies
        # decrease for each dimension. This decay factor is given by:
        #   exp(- log(10000) / (half_dim - 1))
        # You'll use `torch.arange` to create an index range,
        # and then apply the exponential decay to it.

        # Step 3: Multiply frequencies with positions
        # ----------------------------------------------------
        # Multiply each position index in `x` by each frequency in `freqs`.
        # The result should be a tensor of shape (batch_size, seq_length, half_dim).

        # Step 4: Compute sine and cosine
        # ----------------------------------------------------
        # Apply `torch.sin` to one half of `emb` and `torch.cos` to the other half,
        # and concatenate the results along the last dimension.

        # Return the position embedding
        raise NotImplementedError("positional embedding not implemented.")


class MultiHeadSelfAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(MultiHeadSelfAttention, self).__init__()
        self.embed_size = embed_size
        self.heads = heads
        self.head_dim = embed_size // heads

        assert (
                self.head_dim * heads == embed_size
        ), "Embedding size needs to be divisible by heads"

        self.values = nn.Linear(embed_size, embed_size)
        self.keys = nn.Linear(embed_size, embed_size)
        self.queries = nn.Linear(embed_size, embed_size)
        self.fc_out = nn.Linear(embed_size, embed_size)

    def forward(self, values, keys, query, mask):
        """
        Args:
            values: Tensor of shape (N, value_len, embed_size)
            keys: Tensor of shape (N, key_len, embed_size)
            query: Tensor of shape (N, query_len, embed_size)
            mask: Tensor used to mask certain positions (optional)

        Returns:
            out: Output tensor of shape (N, query_len, embed_size)
            attention: Attention weights of shape (N, heads, query_len, key_len)
        """
        # Step 1: Apply Linear Transformations for Queries, Keys, Values
        # ---------------------------------------------------------------
        # Use the layers defined in __init__ to transform values, keys, and query.
        # Each should be transformed to (N, seq_len, embed_size) where
        # seq_len is the length of values, keys, or query.

        # Step 2: Reshape for Multiple Heads
        # ---------------------------------------------------------------
        # Reshape each of values, keys, and queries to split into `heads` pieces.
        # The new shape should be (N, seq_len, heads, head_dim), where head_dim
        # is `embed_size // heads`.

        # Step 3: Compute Scaled Dot-Product Attention
        # ---------------------------------------------------------------
        # Perform the dot-product between queries and keys, then scale by the square root
        # of the embedding dimension for stability.
        # Use `torch.einsum` with "nqhd,nkhd->nhqk" for (N, heads, query_len, key_len).

        # Step 4: Apply Mask (optional)
        # ---------------------------------------------------------------
        # If a mask is provided, use `energy.masked_fill` to set positions where
        # mask == 0 to a very low value (e.g., float("-1e20")). This ensures these
        # positions don’t contribute to attention.

        # Step 5: Compute Attention Weights
        # ---------------------------------------------------------------
        # Apply softmax to normalize the energy tensor across key_len dimension
        # to obtain attention scores, and divide by sqrt(embed_size) for stability.

        # Step 6: Compute Attention Output
        # ---------------------------------------------------------------
        # Use `torch.einsum` to compute weighted sum of values using the attention
        # scores: einsum with "nhql,nlhd->nqhd", then reshape back to (N, query_len, embed_size).

        # Step 7: Final Linear Transformation
        # ---------------------------------------------------------------
        # Pass the output through the final linear layer (self.fc_out).

        # Return the output and attention scores
        # return out, attention
        raise NotImplementedError("MultiHeadSelfAttention not implemented.")


class MiniTransformerEncoder(nn.Module):
    """
    This class implements a simplified Transformer model for sequence classification.
    It uses an embedding layer for tokens, sinusoidal positional embeddings,
    a single Transformer block, and a final linear layer for prediction.

    Args:
      num_vocab: The number of unique tokens in the vocabulary.
      output_size: The size of the output layer (number of classes).
      hidden_size: The dimension of the hidden layer in the Transformer block.
      num_heads: The number of heads in the multi-head attention layer.
    """

    def __init__(self, num_vocab, output_size, hidden_size, heads, device):
        super(MiniTransformerEncoder, self).__init__()

        # Create an embedding for each token
        self.embedding = nn.Embedding(num_vocab, hidden_size)
        self.embedding.weight.data = 0.001 * self.embedding.weight.data  # Computations with multi-head self-attention can be sensitive to input magnitude. Small initial values for embeddings contribute to the stability of these operations.

        self.pos_emb = PositionalEmbedding(hidden_size, device)

        self.multihead_attn_block = MultiHeadSelfAttention(hidden_size,
                                                           heads)  # you cannot call torch.nn.MultiheadAttention, you need to implement your own MultiheadSelfAttention.

        self.feedforward_block = nn.Sequential(nn.Linear(hidden_size, hidden_size),
                                               nn.LayerNorm(hidden_size),
                                               nn.ELU(),
                                               nn.Linear(hidden_size, hidden_size))

        self.fc_out = nn.Linear(hidden_size, output_size)
        self.device = device

    def forward(self, input_seq):
        """
        Args:
            input_seq (torch.Tensor): Input tensor of shape (batch_size, sequence_length).

        Returns:
            torch.Tensor: Output logits of shape (batch_size, sequence_length, output_size).
            torch.Tensor: Attention map of shape (batch_size, heads, sequence_length, sequence_length).
        """
        # Step 1: Embed the input sequence
        # ---------------------------------------------------------------
        # Use the embedding layer to convert input tokens into embeddings.
        # `input_embs` should be of shape (batch_size, sequence_length, hidden_size).

        # Step 2: Generate Positional Embeddings
        # ---------------------------------------------------------------
        # Generate positional embeddings using the SinusoidalPosEmb class.
        # Then, expand them to match the batch size and add them to `input_embs`
        # to incorporate position information.

        # Step 3: Create the Source Mask
        # ---------------------------------------------------------------
        # Create a mask to prevent attention to padding tokens.
        # The mask should be True for real tokens and False for padding tokens.
        # `src_mask` should have the shape (batch_size, 1, 1, sequence_length).

        # Step 4: Apply Multi-Head Self-Attention. This PA requires implementing Multi head self attention by yourself, calling torch.nn.MultiHeadAttention is NOT allowed
        # ---------------------------------------------------------------
        # Pass the embeddings and source mask to `self.multihead_attn_block`.
        # Use `embs` for all three arguments (values, keys, queries).
        # This will produce the `output` and `attn_map`.

        # Step 5: Apply the Feedforward Block
        # ---------------------------------------------------------------
        # Pass the output of the attention block through the feedforward network.
        # The output shape should remain (batch_size, sequence_length, hidden_size).

        # Step 6: Final Output Layer
        # ---------------------------------------------------------------
        # Pass the result through the final linear layer to get the logits.
        # The output shape should be (batch_size, sequence_length, output_size).

        # return output, attn_map
        raise NotImplementedError("MiniTransformerEncoder not implemented.")