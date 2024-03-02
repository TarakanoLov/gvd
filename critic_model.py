from keras.models import Model
from keras.layers import AlphaDropout, Dense, Input, concatenate, Flatten, Multiply, Dropout, BatchNormalization, LeakyReLU, Softmax
from keras.optimizers import SGD, Adam, RMSprop, Nadam
import keras
from keras import backend as K
import tensorflow as tf

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.svm import SVC
import sklearn
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import MiniBatchDictionaryLearning
from sklearn.multiclass import OneVsOneClassifier


from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from contextualbandits.online import BootstrappedUCB, BootstrappedTS, \
            SeparateClassifiers, EpsilonGreedy, AdaptiveGreedy, ExploreFirst, \
            ActiveExplorer, SoftmaxExplorer
from copy import deepcopy

import numpy as np

def keras_custom_loss(y_actual, y_predicted):
    error = K.abs(y_actual - y_predicted)
    clipped_error = tf.clip_by_value(error, 0.0, 1.0)
    linear_error  = 2 * (error - clipped_error)
    return K.square(clipped_error) + linear_error

def make_shok_critic():
    input = Input(shape=(628,))
    x = BatchNormalization()(input)
    x = Dropout(0.2)(x)
    x = Dense(256, activation='selu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    x = Dense(256, activation='selu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    output = Dense(1, activation='tanh')(x)

    model = Model(input, output, name="encoder")
    opt = Nadam(lr=0.00005)
    model.compile(optimizer=opt, loss='mse')
    return model
    
#tf.keras.mixed_precision.experimental.set_policy('mixed_float16')
def make_critic_model():
    board_input = Input(shape=(628,))
    #l = tf.keras.layers.LayerNormalization(axis=1)
    #x = l(board_input)
    x = BatchNormalization()(board_input)
    #x = AlphaDropout(0.05)(x)
    x = Dense(128, activation='selu')(x)
    x = BatchNormalization()(x)
    #x = Dropout(0.2)(x)
    x = Dense(64, activation='selu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)

    value_output = Dense(1, activation='tanh')(x)

    model = Model(inputs=board_input, outputs=value_output)
    
    #opt = Nadam(lr=0.00005)
    opt = Nadam(lr=0.001)
    model.compile(loss=keras_custom_loss, optimizer=opt, metrics=['mae', 'mse'])
    return model

