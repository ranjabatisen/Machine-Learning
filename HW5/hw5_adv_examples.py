# -*- coding: utf-8 -*-
"""hw5_adv_examples.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AI1bv779xfKheQLoJhYGIXVxK7Hwd6C4
"""

import torch
import torchvision
from torchvision import transforms
from torchvision.models import resnet50
from pandas import read_json
from torch.autograd import Variable
from torch.autograd.gradcheck import zero_gradients
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

def calc_loss(pred_vector, i):
    Loss = nn.CrossEntropyLoss()
    y = Variable(torch.LongTensor([i]), requires_grad=False)
    loss = Loss(pred_vector, y)
    loss.backward()

def show_img(z, i, x):
    plt.figure(i)
    z = z.squeeze(0)
    z = z.mul(torch.FloatTensor([0.229, 0.224, 0.225]).view(3,1,1)).add(torch.FloatTensor([0.485, 0.456, 0.406]).view(3,1,1)).detach().numpy()
    plt.title("Part " + x)
    plt.imshow(np.transpose( z , (1,2,0)) )

def classify(pred_vector, labels, x):
    _, idx = torch.max(pred_vector, 1)
    class_name = labels[idx.numpy()[0]][1]
    print("Label in part " + x + " : " + class_name)

def A(normalized_my_tensor, model, labels):
    # fast gradient signed method
    image_var = Variable(normalized_my_tensor, requires_grad=True)
    image_var.data = normalized_my_tensor
    zero_gradients(image_var)
    pred_vector1 = model(image_var)
    calc_loss(pred_vector1, 1)
    noise = image_var.data - (0.03 * torch.sign(image_var.grad.data)) - normalized_my_tensor
    noise = torch.clamp(noise, -0.3, 0.3)
    image_var.data = normalized_my_tensor + noise
    pred_vector2 = model(image_var)
    classify(pred_vector2, labels, "a")
    show_img(image_var, 1, "a")

def B(normalized_my_tensor, model, labels):
    # fast gradient signed method
    image_var = Variable(normalized_my_tensor, requires_grad=True)
    image_var.data = normalized_my_tensor
    for k in range(5):
        zero_gradients(image_var)
        pred_vector1 = model(image_var)
        calc_loss(pred_vector1, 466)
        noise = image_var.data - (0.03 * torch.sign(image_var.grad.data)) - normalized_my_tensor
        noise = torch.clamp(noise, -0.3, 0.3)
        image_var.data = normalized_my_tensor + noise
    pred_vector2 = model(image_var)
    classify(pred_vector2, labels, "b")
    show_img(image_var, 2, "b")

def main():
    model = resnet50(pretrained=True)
    my_img = plt.imread("Elephant2.jpg") 
    model = resnet50(pretrained=True).eval()
    preprocess = transforms.Compose([transforms.ToPILImage(),transforms.Resize(224),transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),])
    normalized_my_tensor = preprocess(my_img)[None,:,:,:]
    pred_vector = model(normalized_my_tensor)
    labels = read_json('imagenet_class_index.json')
    # Find label of class classified by resnet
    classify(pred_vector, labels, "1")
    # Part a of problem
    A(normalized_my_tensor, model, labels)
    # part b of problem
    B(normalized_my_tensor, model, labels)
    

if __name__== "__main__":
    main()