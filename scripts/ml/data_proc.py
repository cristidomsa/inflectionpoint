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

  