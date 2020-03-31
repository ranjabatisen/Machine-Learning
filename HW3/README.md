# Machine Learning Homework 3

Implemented a muli-layer fully connected neural network and a convolutional neural network using pytorch on MNIST dataset.

For the fully connected neural network :
```
1. Input: 1-channel input, size 28x28
2. Keep batch size as 32.
3. Fully connected layer 1: Input with bias; output - 128
4. ReLu Layer
5. Fully connected layer 2: input - 128; output - 10
6. Softmax layer
7. Use cross entropy as loss function
8. Use SGD as optimizer.
```

For the cnn:
```
1. Input: 1-channel input, size 28x28
2. Keep batch size as 32.
3. Convolution layer: Convolution kernel size is (3, 3) with stride as 1. Input channels - 1; Output channels - 20
4. Max-pool: 2x2 max pool
5. ReLu Layer
6. Flatten input for feed to fully connected layers
7. Fully connected layer 1: flattened input with bias; output - 128
8. ReLu Layer
9. Fully connected layer 2: input - 128; output - 10
10. Softmax layer as above
11. Use cross entropy as loss function
12. Use SGD as optimizer.
```
