# Distributed Tensorflow 1.9 Example

Distributed tensorflow is mainly used when you want to train your models faster in parallel incase they are time consuming ones and if your model is so big (for ex: Neural network models or language modelings etc.,) that it doesn't fit in single machine then this approach is used. In this process you can use GPUs to run the model faster with better accuracy and results.

This example illustrates the data parallelism with shared model parameters while updating parameters asynchronous.

This model trains a simple sigmoid Neural Network on MNIST for 20 epochs on three machines using one parameter server. The goal was not to achieve high accuracy but to get to know tensorflow.

Run it as following:

First, change the hardcoded host names with your own and run the following commands on the respective machines.

```
pc-01$ python example.py --job_name="ps" --task_index=0 
pc-02$ python example.py --job_name="worker" --task_index=0 
pc-03$ python example.py --job_name="worker" --task_index=1 
pc-04$ python example.py --job_name="worker" --task_index=2 
```
After running the example.py on all nodes, As a first step, MNIST dataset is generated for the training and then the training is started for 20 epochs finally providing the "Test-accuracy", "Total Time" and "Final cost". Each node will provide these three params "Test-accuracy", "Total Time" and "Final cost" and under the hood tensorflow is 

Note:

Neuron(Node) — It is the basic unit of a neural network. It gets certain number of inputs and a bias value. When a signal(value) arrives, it gets multiplied by a weight value. If a neuron has 4 inputs, it has 4 weight values which can be adjusted during training time.

Batch Size — The number of training examples in one forward/backward pass. The higher the batch size, the more memory space you’ll need.

Training Epochs — It is the number of times that the model is exposed to the training dataset.

One epoch = one forward pass and one backward pass of all the training examples.


