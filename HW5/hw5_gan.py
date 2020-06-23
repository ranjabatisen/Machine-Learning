# -*- coding: utf-8 -*-
"""hw5_gan.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18JvI5aRIJrtJuwsiFctR8p_OLisl-xy9
"""

import torch
import torchvision
from torchvision import transforms, datasets
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# downloading data
train = datasets.MNIST(root='./data', train=True, download=True,transform=transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=(0.5,), std=(0.5,))]))

# Mini batches of batch size 100
trainset = torch.utils.data.DataLoader(train, batch_size=100, shuffle=False)

# Generator
class generator(nn.Module):
    def __init__(self):
        super(generator, self).__init__()
        self.fc1 = nn.Linear(128, 256)
        self.relu1 = nn.LeakyReLU(0.2)
        self.fc2 = nn.Linear(256, 512)
        self.relu2 = nn.LeakyReLU(0.2)
        self.fc3 = nn.Linear(512, 784)
        self.tan1 = nn.Tanh()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        out = self.tan1(x)
        return out

# Discriminator
class discriminator(nn.Module):
    def __init__(self):
        super(discriminator, self).__init__()
        self.fc1 = nn.Linear(784, 512)
        self.relu1 = nn.LeakyReLU(0.2)
        self.fc2 = nn.Linear(512, 256)
        self.relu2 = nn.LeakyReLU(0.2)
        self.fc3 = nn.Linear(256, 1)
        self.sig1 = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        out = self.sig1(x)
        return out

def train_gen(gen_optimizer, disc_pred, image_r_y):
    gen_optimizer.zero_grad()
    # binary cross entropy loss
    Loss = nn.BCELoss()
    loss = Loss(disc_pred, image_r_y)
    # back propagation
    loss.backward()
    gen_optimizer.step()
    gloss = loss.item()*100
    return gloss

def train_disc(disc_optimizer, disc_pred, y):
    disc_optimizer.zero_grad()
    # binary cross entropy loss
    Loss = nn.BCELoss()
    loss = Loss(disc_pred, y)
    # back propagation
    loss.backward()
    disc_optimizer.step()
    dloss = loss.item()*100
    return dloss

def calc_loss(gen, disc, gen_optimizer, disc_optimizer, data) :
    k, (image, _) = data
    # real image
    image_r = image.view(image.size(0), -1)
    # generating fake image
    image_f = gen(torch.randn(image.size(0), 128))
    # concatenate the images
    images = torch.cat((image_r, image_f))
    # labels of real images are 1 and fake images are 0
    image_r_y = torch.ones(image.size(0)).view(-1,1) 
    image_f_y = torch.zeros(image.size(0)).view(-1,1) 
    # concatenate the labels
    y = torch.cat((image_r_y, image_f_y))
    dloss = train_disc(disc_optimizer, disc(images), y)
    gloss = train_gen(gen_optimizer, disc(gen(torch.randn(image.size(0), 128))), image_r_y)
    return gloss, dloss

def train_gan(gen, disc, gen_optimizer, disc_optimizer, gen_loss, disc_loss):
    for epoch in range(50):
        gen_sum = 0
        disc_sum = 0
        for data in enumerate(trainset):
            gloss, dloss = calc_loss(gen, disc, gen_optimizer, disc_optimizer, data)
            gen_sum = gen_sum + gloss
            disc_sum = disc_sum + dloss
        gen_loss.append(gen_sum/60000)
        disc_loss.append(disc_sum/60000)
        # generated image grids
        n = (epoch + 1) % 10
        if n == 0:
            imgnew = gen(torch.randn(16, 128)).data
            plt.figure(figsize=[6, 6])
            for i in range(4*4):
                plt.subplot(4, 4, i+1)
                plt.imshow(imgnew[i].reshape(28,28), cmap='gray')
                frame = plt.gca()
                frame.axes.get_xaxis().set_visible(False)
                frame.axes.get_yaxis().set_visible(False)
            plt.subplots_adjust(wspace = 0.05, hspace = 0.05)
            plt.savefig("grid_" + str(epoch + 1) + ".png")
            plt.show()
    # saving trained model
    torch.save(gen, './hw5_gan_gen.pth')
    torch.save(disc, './hw5_gan_dis.pth')
            
def main():
    gen = generator()
    disc = discriminator()
    # Adam as optimizer
    gen_optimizer = optim.Adam(gen.parameters(), lr=0.0002)
    disc_optimizer = optim.Adam(disc.parameters(), lr=0.0002)
    gen_loss = list()
    disc_loss = list()
    # training
    train_gan(gen, disc, gen_optimizer, disc_optimizer, gen_loss, disc_loss)
    plt.plot(gen_loss, label = 'generator loss')
    plt.plot(disc_loss, label = 'discriminator loss')
    plt.ylabel("Loss")
    plt.xlabel("Epochs")
    plt.title("Loss vs Epochs")
    plt.legend()
    plt.show()

if __name__== "__main__":
    main()