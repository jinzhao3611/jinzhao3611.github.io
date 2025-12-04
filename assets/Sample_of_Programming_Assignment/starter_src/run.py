#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jin Zhao
# Date: 11/06/24 17:08
"""Entry point

Feel free to change/restructure the entire project if you wish
"""
from tqdm.notebook import tqdm
import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader

from corpus import PDTBDataset, build_vocab, load_data
from model import MiniTransformerEncoder

# Define the hyperparameters
learning_rate = 1e-4
nepochs = 50
batch_size = 128
max_len = 60 # Maximum sequence length for text inputs
SENSE_LEVEL = 2
heads = 2
hidden_size = 256
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


train_raw, dev_raw, test_raw = load_data(data_dir='your_path/data/pdtb', sense_level=SENSE_LEVEL)

train_tokenized_texts = [['SOS'] + pdtb_relation.features[0] + ['SEP'] +  pdtb_relation.features[1] + ['SEP'] + pdtb_relation.features[2] +['EOS'] for pdtb_relation in train_raw]
vocab = build_vocab(train_tokenized_texts)
unique_labels = set([relation.label for relation in train_raw if relation.label is not None])
label_to_index = {label: idx for idx, label in enumerate(unique_labels)}
index_to_label = {idx: label for label, idx in label_to_index.items()}

train_dataset = PDTBDataset(train_raw, vocab, max_len, label_to_index)
dev_dataset = PDTBDataset(dev_raw, vocab, max_len, label_to_index)
test_dataset = PDTBDataset(test_raw, vocab, max_len, label_to_index)

# Create data loaders for the training and testing datasets
data_loader_train = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
data_loader_dev = DataLoader(dev_dataset, batch_size=batch_size)
data_loader_test = DataLoader(test_dataset, batch_size=batch_size)

classifier = MiniTransformerEncoder(num_vocab=len(vocab), output_size=16, hidden_size=hidden_size, heads=heads, device=device).to(device)
optimizer = optim.Adam(classifier.parameters(), lr=learning_rate)
lr_scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=nepochs, eta_min=0)
# lr_scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=nepochs, gamma=0.5)
loss_fn = nn.CrossEntropyLoss()


train_acc = 0
dev_acc = 0

# Loop over each epoch
for epoch in range(nepochs):
    train_acc_count = 0
    dev_acc_count = 0

    # Set the model to training mode
    classifier.train()
    steps = 0

    # Loop over each batch in the training dataset
    for label, text in tqdm(data_loader_train, desc="Training", leave=False):
        text = text.to(device)
        label = label.to(device)

        # Get the model predictions
        pred, _ = classifier(text)

        # Compute the loss using cross-entropy loss
        loss = loss_fn(pred[:, 0, :], label)

        # Backpropagation and optimization step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Log the training loss
        print("train loss:", loss.item())

        # Update training accuracy
        train_acc_count += (pred[:, 0, :].argmax(1) == label).sum()
        steps += batch_size

    # Calculate average training accuracy
    train_acc = (train_acc_count / steps).item()
    print("train accuracy: ", train_acc)

    # Update learning rate
    lr_scheduler.step()

    # Set the model to evaluation mode
    classifier.eval()
    steps = 0

        # Loop over each batch in the dev dataset
    with torch.no_grad():
        for label, text in tqdm(data_loader_dev, desc="dev", leave=False):

            # Transform the text to tokens and move to the GPU
            text = text.to(device)
            label = label.to(device)

            # Get the model predictions
            pred, _ = classifier(text)

            # Compute the loss using cross-entropy loss
            loss = loss_fn(pred[:, 0, :], label)
            print("dev loss: ", loss.item())

            # Update dev accuracy
            dev_acc_count += (pred[:, 0, :].argmax(1) == label).sum()
            steps += batch_size

        # Calculate average dev accuracy
        dev_acc = (dev_acc_count / steps).item()
        print("dev accuracy", dev_acc)

