## import required libraries

from sklearn.model_selection import train_test_split
import math
import pandas as pd
import numpy as np
import tensorflow as tf
import random

### building a class to convert time series to images

# defining variables of the class

class MakeImage:

    def __init__(self):

        self._df = None
        self._size_width = None
        self._index_of_columns_2_be_batched = None
    
    # defining setters and getters
    @property     
    def df(self):
        return self._df   

    @property
    def size_width(self):
        return self._size_width

    @property
    def index_of_columns_2_be_batched(self):
        return self._index_of_columns_2_be_batched

     @df.setter
     def df(self, value):
        self._df = pd.read_excel(value, 0, names = ["load_data"])

    @size_width.setter
    def size_width(self, value):
        self._size_width = value

     @index_of_columns_2_be_batched.setter
     def index_of_columns_2_be_batched(self, value):
        self._index_of_columns_2_be_batched = value

    def add_label(self):
        df = self.df
        df.ix[0,'label'] = 0.0
        df.ix[1:,'label'] = [1.0 if df.ix[i,'load_data'] > df.ix[i-1,'load_data'] else 0.0  for i in range(1,len(df.index))]
        
    def chunk_features_and_label(self, col_name, col_label):

        df = self.df
        image_width = self.size_width
        nparray_features = np.zeros(shape = (len(df.index) - image_width, image_width))
        nparray_label = np.zeros(shape = (len(df.index) - image_width, 1))

        for i in range(len(df.index) - image_width):
                nparray_features[i, :] = df.ix[i: i + image_width - 1, col_name].as_matrix().reshape(image_width)
                nparray_label[i, :] = df.ix[i + image_width, col_label].reshape(-1,1)

        return nparray_features, nparray_label
    def features_2_images(self, x):

        size_width = self.size_width

        x_image = np.zeros(shape = (x.shape[0], x.shape[1]*x.shape[1]))

        print(x.shape[0])

        for i in range(x.shape[0]):

            x_temp = x[i, :].copy()

            x_copy = np.copy(x[i,:])

            x_int = np.zeros(shape = (x_copy.shape), dtype = int)

            x_copy2 = np.copy(x[i,:])

            x_copy.sort()

            for j in range(np.size(x_copy)):

                for k in range(np.size(x_copy)):

                    if x_copy2[j] == x_copy[k]:

                        x[i, j] = int(k)

            n_values = np.max(x[i,:].astype(int)) + 1

            squared = np.eye(n_values)[x[i,:].astype(int)]

            flatten = squared.flatten()

            x_image[i, :] = flatten

        return x_image

    def convert_2_onehot_encoding(self, vector_of_one_dim):

        nparray_lab_onehot = np.zeros(shape = (vector_of_one_dim.shape[0], 2))

        for i in range(vector_of_one_dim.shape[0]):

            n_values = 2
            nparray_lab_onehot[i, :] = np.eye(n_values)[vector_of_one_dim[i,:].astype(int)]           

        return nparray_lab_onehot

    def number_of_batches(self, x, batch_size):

        return int(x.shape[0]/batch_size)

    def next_batch(self, x, y, batch_size):

        index_for_batch = self.index_of_columns_2_be_batched

        if len(index_for_batch) >= batch_size:
            selected_index = random.sample(index_for_batch, batch_size)
        else:
            selected_index = random.sample(index_for_batch, len(index_for_batch))    

        x_batch = [x[i] for i in selected_index]
        y_batch = [y[i] for i in selected_index]

        self.index_of_columns_2_be_batched = [i for i in index_for_batch if i not in selected_index]

        return x_batch, y_batch

### create a class and initialize an instance of it

def cnn_model():
    # building computation graph

    # the input images are 32*32, so flattened images are a size of 1024
    x = tf.placeholder(tf.float32, [None, 1024])   

    # because we have just two labels
    y = tf.placeholder(tf.float32, [None, 2])

    # the input images are 32*32        
    input_layer_of_load_images = tf.reshape(x, [-1, 32, 32, 1])

    # covulate layer 1 specifications are
    convolute_layer_1 = tf.layers.conv2d(
                                        inputs = input_layer_of_load_images,
                                        filters = 32,
                                        kernel_size = [5, 5],
                                        padding = "same",
                                        activation = tf.nn.relu)

    # pooling layer 1 specifications are
    pool_layer_1 = tf.layers.max_pooling2d(
                                            inputs=convolute_layer_1,
                                            pool_size=[2, 2],
                                            strides=2)
    #  covulate layer 2 specifications are

    convolute_layer_2 = tf.layers.conv2d(
                                        inputs=pool_layer_1,
                                        filters=64,
                                        kernel_size=[5, 5],
                                        padding="same",
                                        activation=tf.nn.relu)
    # pooling layer 2 specifications are

    pool_layer_2 = tf.layers.max_pooling2d(
                                        inputs = convolute_layer_2,
                                        pool_size=[2, 2],
                                        strides=2)
    # pooling layer 2 output is going to be flattened as follows to be the input for the next layer
    pool_layer_2_flat = tf.reshape(pool_layer_2,[-1, 8 * 8 * 64])
    # dense layer 1 specifications are

    dense_layer_1 = tf.layers.dense(inputs = pool_layer_2_flat,
                                    units=1024,
                                    activation=tf.nn.relu)

    # dense layer 2 specifications are

    dense_layer_2 = tf.layers.dense(inputs = dense_layer_1,
                                    units = 600,
                                    activation=tf.nn.relu)
    # using dropout technique to avoid overfitting, which shuts down neurons at a rate of 40%
    dropout = tf.layers.dropout(
                                inputs = dense_layer_2, rate = 0.4)
    # dense layer 3 specifications are
    dense_layer_3 = tf.layers.dense(inputs = dropout,
                                    units=400)

 

    # prediction and final outputs
    prediction = tf.layers.dense(dense_layer_3, activation=tf.nn.softmax, units = 2)
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y * tf.log(prediction), reduction_indices=[1]))  
    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
    number_of_epochs = 15

    # creating  session for running computation graph

    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())

        for epoch in range(number_of_epochs):

            epoch_loss = 0

            makeImage.index_of_columns_2_be_batched = [i for i in range(0, X_train.shape[0])]

            for _ in range(number_of_batches):

                            epoch_x, epoch_y = makeImage.next_batch(X_train, y_train, batch_size)

                            _, c = sess.run([train_step, cross_entropy], feed_dict={x: epoch_x, y: epoch_y})

                            epoch_loss += c

        print('Epoch', epoch + 1, 'completed out of', number_of_epochs,' with loss:',epoch_loss)

                correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

                accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        print('Accuracy in epoch', epoch + 1, 'is:',accuracy.eval({x:X_test, y:y_test}))



makeImage = MakeImage()

## Setter instance variables
#  put the path of your time series data in your system as shown below

path_2_excel_file = 'path to data/load_data.xlsx'

makeImage.df = path_2_excel_file  # a string that shows path of data

# set the image size (we determined for this application that 32 is a good choice)

makeImage.size_width = 32

makeImage.columns_2_pad = ['load_data', 'label']

makeImage.add_label()

# process load data to be proper for the model

X_not_ready_yet, Y_not_ready_yet = makeImage.chunk_features_and_label('load_data', 'label')
X_ready = makeImage.features_2_images(X_not_ready_yet)
Y_ready = makeImage.convert_2_onehot_encoding(Y_not_ready_yet)

# select 70% of data for training the model and 30% for testing
X_train, X_test, y_train, y_test = train_test_split(X_ready, Y_ready, test_size = 0.3) 

# the batch size is selected to be 100; it is possible to adjust it based on the problem’s requirements

batch_size = 100

# we need to calculate number of batches
number_of_batches = makeImage.number_of_batches(X_train, batch_size)

cnn_model()
