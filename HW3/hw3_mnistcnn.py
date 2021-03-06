# -*- coding: utf-8 -*-
"""hw3_mnistcnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zOUciWrUdsqW5UWXZ_KSr7Jrve46ne7O
"""

import torch
import torchvision
from torchvision import transforms, datasets
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import time

# downloading data
train = datasets.MNIST(root='./data', train=True, download=True,transform=transforms.Compose([transforms.ToTensor()]))
test = datasets.MNIST(root='./data', train=False, download=True,transform=transforms.Compose([transforms.ToTensor()]))

# Mini batches of batch size 32
trainset = torch.utils.data.DataLoader(train, batch_size=32, shuffle=True)
testset = torch.utils.data.DataLoader(test, batch_size=32, shuffle=False)

# Fully connected neural network
class net(nn.Module):
    def __init__(self):
        super(net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, kernel_size=3)
        self.fc1 = nn.Linear(13*13*20, 128)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # ReLu on 2x2 max-pool layer on convolution layer
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = x.view(-1, 13*13*20 )
        x = self.fc1(x)
        # ReLu layer
        x = self.relu1(x)
        x = self.fc2(x)
        # softmax layer
        out = F.log_softmax(x, dim=1)
        return out

def train_net(cnn, optimizer, train_loss, train_accuracy):
    num_epochs = 200
    prev_loss = 50
    for epoch in range(num_epochs):
        correct = 0
        total = 0
        for data in trainset:
            # data is every batch with X as features and y as classes
            X, y = data  
            # set gradient = 0
            optimizer.zero_grad()
            # forward pass the batch
            output = cnn(X)
            # cross entropy loss calculation
            loss = F.cross_entropy(output, y)
            # back propagation
            loss.backward()  
            # optimize parameters based on gradient/loss
            optimizer.step()
            # to calculate accuracy
            total += y.shape[0]    
            _, predict = output.max(1)
            correct += (predict == y).sum().item()
        train_loss.append(loss.item())
        # accuracy = no. of correct predictions/size of data
        train_accuracy.append(round(correct/total, 3))
        # check for convergence
        if abs(loss.item() - prev_loss) < 0.002 and loss.item() < 0.05:
           break
        else:
           prev_loss = loss.item()
    # saving trained model
    torch.save(cnn, './mnist-cnn.pt')

def test_net():
    # Load trained model
    cnn = torch.load('./mnist-cnn.pt')
    correct = 0
    total = 0
    with torch.no_grad():
        for features, classes in testset:
            out = cnn(features)
            for index in enumerate(out):
                class_index, pred_index = index
                if torch.argmax(pred_index) == classes[class_index]:
                    correct += 1
                total += 1
    # Testing accuracy
    print("Test accuracy: ", round(correct/total, 3))

def train_net1(cnn, optimizer, trainset1):
    num_epochs = 200
    prev_loss = 50
    start_time = time.time()
    for epoch in range(num_epochs):
        correct = 0
        total = 0
        for data in trainset1:
            # data is every batch with X as features and y as classes
            X, y = data  
            # set gradient = 0
            optimizer.zero_grad()
            # forward pass the batch
            output = cnn(X)
            # cross entropy loss calculation
            loss = F.cross_entropy(output, y)
            # back propagation
            loss.backward()  
            # optimize parameters based on gradient/loss
            optimizer.step()
        # check for convergence
        if abs(loss.item() - prev_loss) < 0.002 and loss.item() < 0.05:
           break
        else:
           prev_loss = loss.item()
    return (time.time() - start_time)/60


def batch_size_vary(learning_rate):
    batch_size = [32, 64, 96, 128]
    runtime = list()
    for batch in batch_size:
        cnn = net()
        optimizer = optim.SGD(cnn.parameters(), lr=learning_rate)
        trainset1 = torch.utils.data.DataLoader(train, batch_size=batch, shuffle=True)
        time = train_net1(cnn, optimizer, trainset1) 
        runtime.append(time)
    # Plot of convergence run time vs batch sizes
    plt.plot(batch_size, runtime)
    plt.ylabel("Convergence runtime")
    plt.xlabel("Batch size")
    plt.title("Convergence run time vs batch sizes")
    plt.show()

def optimizer_vary(learning_rate):
    cnn = net()
    # SGD as optimizer
    optimizer = optim.SGD(cnn.parameters(), lr=learning_rate)
    train_loss1 = list()
    train_accuracy = list()
    # train the model
    train_net(cnn, optimizer, train_loss1, train_accuracy)
    cnn = net()
    # Adam as optimizer
    optimizer = optim.Adam(cnn.parameters(), lr=0.0001)
    train_loss2 = list()
    train_accuracy = list()
    # train the model
    train_net(cnn, optimizer, train_loss2, train_accuracy)
    cnn = net()
    # Adagrad as optimizer
    optimizer = optim.Adagrad(cnn.parameters(), lr=learning_rate)
    train_loss3 = list()
    train_accuracy = list()
    # train the model
    train_net(cnn, optimizer, train_loss3, train_accuracy)
    # Plot of loss vs epoch for each optimizer
    plt.plot(train_loss1, label = "SGD")
    plt.plot(train_loss2, label = "Adam")
    plt.plot(train_loss3, label = "Adagrad")
    plt.ylabel("Training Loss")
    plt.xlabel("Epoch")
    plt.title("Loss vs Epoch for every optimizer")
    plt.legend()

def main():
    cnn = net()
    learning_rate = 0.001
    # SGD as optimizer
    optimizer = optim.SGD(cnn.parameters(), lr=learning_rate)
    train_loss = list()
    train_accuracy = list()
    # train the model
    train_net(cnn, optimizer, train_loss, train_accuracy)
    # Check convergence of loss function
    plt.figure(1)
    plt.plot(train_loss)
    plt.ylabel("Training Loss")
    plt.xlabel("Epoch")
    plt.title("Loss Function for SGD optimizer")
    plt.show()
    # Accuracy plot
    plt.figure(2)
    plt.plot(train_accuracy)
    plt.ylabel("Training Accuracy")
    plt.xlabel("Epoch")
    plt.title("Accuracy")
    plt.show()
    # test the model
    test_net()
    # vary batch sizes and compare convergence run time
    batch_size_vary(learning_rate)
    # check loss curve for each optimizer
    optimizer_vary(learning_rate)

if __name__== "__main__":
    main()