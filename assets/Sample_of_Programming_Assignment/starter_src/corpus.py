#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jin Zhao
# Date: 11/06/24 17:08
"""
feel free to add your own hyperparameters and change code anywhere

NOTE
    1. regular `.py` files and the jupyter notebook are organized slightly differently,
        although the underlying logic is the same
    3. default values below are arbitrary and should be modified during experiments
"""

import numpy as np
import os
import codecs
import json
from typing import List, Optional, Tuple, Dict
from collections import Counter

import torch
from torch.utils.data.dataset import Dataset


class PDTBRelation:
  """A single PDTB relation data instance"""
  def __init__(self,
               arg1: str,
               arg2: str,
               connective: Optional[str] = None,
               label: str = None,
               stype: str = None):
    # raw data and label
    self.arg1 = arg1
    self.arg2 = arg2
    self.connective = connective # may be empty if implicit relations
    self.label = label
    self.stype = stype

    # raw features
    self.features = self.featurize() # type: Tuple[List[str], List[str], List[str]]

    # numeric features as numpy ndarray
    self.feature_vector = []  # type: np.ndarray

  def featurize(self) -> Tuple[List[str], List[str], List[str]]:
    """Trivially tokenized words"""
    return self.arg1.split(), self.arg2.split(), self.connective.split()

  def featurize_vector(self, vocab=None) -> np.ndarray:
    arg1_vocab, arg2_vocab, conn_vocab = vocab
    num_feats = len(arg1_vocab) + len(arg2_vocab) + len(conn_vocab)

    idx_space = [0, len(arg1_vocab), len(arg1_vocab) + len(arg2_vocab)]

    # construct feature vector based on vocab
    feature_vector = np.zeros(num_feats+1, dtype=np.int)
    for i, (features, feat_vocab) in enumerate(zip(self.features, vocab)):
      for token in features:
        if token in feat_vocab:
          # accumulate feature counts
          tok_idx = feat_vocab.index(token)
          tok_idx = idx_space[i] + tok_idx

          feature_vector[tok_idx] += 1
    feature_vector[-1] = 1  # bias
    self.feature_vector = feature_vector
    return feature_vector


def to_level(sense: str, level: int = 2) -> str:
  s_split = sense.split(".")
  s_join = ".".join(s_split[:level])
  return s_join
def load_relations(file_path, sense_level=2):
  data = []
  with codecs.open(file_path, encoding='utf-8') as pdtb:
    pdtb_lines = pdtb.readlines()
    for pdtb_line in pdtb_lines:
      rel = json.loads(pdtb_line)

      arg1 = rel['Arg1']['RawText']
      conn = rel['Connective']['RawText']
      arg2 = rel['Arg2']['RawText']
      label = to_level(rel['Sense'][0], level=sense_level)  # always the first sense
      stype = rel['Type']

      doc = PDTBRelation(arg1, arg2, conn, label, stype)
      data.append(doc)
  return data

def load_data(data_dir, sense_level=2):
  data = {}
  for filename in os.listdir(data_dir):
    if not filename.endswith('.json'):
      continue

    dataset_type = os.path.splitext(filename)[0]
    rel_file = os.path.join(data_dir, filename)
    data[dataset_type] = load_relations(rel_file, sense_level=sense_level)

  return data['train'], data['dev'], data['test']

def yield_tokens(train_raw):
  for pdtb_relation in train_raw:
    yield pdtb_relation.features[0] + pdtb_relation.features[1] + pdtb_relation.features[2]

def build_vocab(tokenized_texts: List[List[str]], min_freq: int = 1) -> Dict[str, int]:
    counter = Counter([token for text in tokenized_texts for token in text])
    vocab = {token: idx for idx, (token, freq) in enumerate(counter.items(), start=2) if freq >= min_freq}
    vocab["<PAD>"] = 0  # Padding token
    vocab["<UNK>"] = 1  # Unknown token for out-of-vocabulary words
    return vocab

def encode(text: List[str], vocab: Dict[str, int]) -> List[int]:
    return [vocab.get(token, vocab["<UNK>"]) for token in text]

def pad_or_truncate_sequences(sequences: List[List[int]], max_length: int = 60, pad_token: int = 0) -> torch.Tensor:
    processed_sequences = []
    for seq in sequences:
        if len(seq) > max_length:
            # Truncate if the sequence is longer than max_length
            processed_seq = seq[:max_length]
        else:
            # Pad if the sequence is shorter than max_length
            processed_seq = seq + [pad_token] * (max_length - len(seq))
        processed_sequences.append(processed_seq)

    return torch.tensor(processed_sequences, dtype=torch.long)


class PDTBDataset(Dataset):
    def __init__(self, relations: List[PDTBRelation], vocab, max_len, label_to_index):
        """
        Initializes the dataset with a list of PDTBRelation objects.

        Args:
            relations (List[PDTBRelation]): List of PDTBRelation objects.
            vocab (dict): Dictionary mapping tokens to indices.
            max_len (int): Maximum sequence length for padding/truncating.
        """
        # Step 1: Store the provided arguments in instance variables
        # ---------------------------------------------------------------
        # Initialize self.relations, self.vocab, and self.max_length
        raise NotImplementedError("pdtb dataset not implemented.")


    def __len__(self):
        """Returns the number of samples in the dataset."""
        # Step 2: Return the length of self.relations to indicate the
        #         total number of samples in the dataset.
        raise NotImplementedError("pdtb dataset not implemented.")


    def __getitem__(self, idx):
        """
        Retrieves a sample from the dataset at the specified index.

        Args:
            idx (int): Index of the sample to retrieve.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: The label tensor and tokenized text tensor.
        """
        # Step 3: Retrieve the PDTBRelation object at the specified index
        # ---------------------------------------------------------------
        # Use idx to access the relation from self.relations.

        # Step 4: Tokenize and Encode the Text
        # ---------------------------------------------------------------
        # 4.1 - Concatenate features with special tokens.
        #       Example: ['SOS'] + feature1 + feature2 + ['SEP'] + feature3 + ['EOS']

        # 4.2 - Convert tokens to indices using the vocabulary.
        #       Use the provided `encode` function to convert tokenized_text to a list of indices.

        # Step 5: Pad or Truncate the Sequence
        # ---------------------------------------------------------------
        # Use the `pad_or_truncate_sequences` function to ensure the encoded_text
        # matches the max_length. Pad with self.vocab["<PAD>"] if the sequence is too short.

        # Step 6: Convert Encoded Text to Tensor
        # ---------------------------------------------------------------
        # Convert padded_truncated_text to a tensor of dtype torch.long and remove
        # any extra batch dimension by using `squeeze(0)`.

        # Step 7: Encode the Label
        # ---------------------------------------------------------------
        # Convert the label to an index using label_to_index and convert it to a tensor.
        # The label should be of dtype torch.long.

        # Step 8: Return the Label and Encoded Text Tensors
        # return label, text_tensor
        raise NotImplementedError("pdtb dataset not implemented.")
