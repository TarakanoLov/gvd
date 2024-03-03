from keras.models import Model
from keras.layers import Dense, Input, concatenate, Flatten, Multiply, Dropout, BatchNormalization, LeakyReLU, Softmax, Add, Lambda, Reshape
from keras.optimizers import SGD, RMSprop, Adam, Nadam
import keras
import tensorflow as tf
import tensorflow_probability as tfp

import numpy as np

from sklearn.linear_model import LogisticRegression
#from contextualbandits.online import BootstrappedUCB, BootstrappedTS, \
 #           SeparateClassifiers, EpsilonGreedy, AdaptiveGreedy, ExploreFirst, \
  #          ActiveExplorer, SoftmaxExplorer
from copy import deepcopy


def make_model():
    n_inputs = 2 + 2 + 6 + 6 #+ (34 + 34 + 34) #* 2
    
    
    
    return bootstrapped_ucb

from keras import backend as K

#def keras_custom_loss_1(y_actual, y_predicted):
#    return K.max(K.abs(y_actual - y_predicted), axis=1)

def keras_custom_loss(y_actual, y_predicted):
    return K.max(K.abs(y_actual - y_predicted), axis=1)*K.max(K.abs(y_actual - y_predicted), axis=1)

from tensorflow.keras import layers

class ReductionLayer(layers.Layer):
    def __init__(self):
        super(ReductionLayer, self).__init__()

    def call(self, inputs):
        return tf.reduce_sum(inputs, axis=0)

def make_model_test():
    n_inputs = 2 + 2 + 6 + 6 #+ (34 + 34 + 34) #* 2
    
    board_input = Input(shape=(n_inputs,), name='board_input')
    #x = BatchNormalization()(board_input)
    #x = tf.keras.layers.experimental.preprocessing.Normalization(board_input)
    x = Dense(64, activation='selu')(board_input)
    #x = BatchNormalization()(x)
    x = Dense(64, activation='selu')(x)
    #x = BatchNormalization()(x)
    #x = Dropout(0.2)(x)
    #action_layer3 = Dense(32, activation='relu')(action_layer2)
    #action_layer4 = Dense(32, activation='relu')(action_layer3)
    #action_layer5 = Dense(32, activation='relu')(action_layer4)
    #action_layer6 = Dense(32, activation='relu')(action_layer5)
    
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')
    
    
    #use_and_drop = concatenate([board_layer2, action_layer2], axis=1, name='board_and_action')
    policy_output = Multiply()([action_input, Dense(34 * 3 * 2, activation='tanh')(x)])
    

    model = Model(inputs=[board_input, action_input], outputs=policy_output)
    #opt = SGD(lr=0.000000001)
    #opt = Nadam(lr=0.00001)
    opt = Nadam(learning_rate=0.001)
    #opt = RMSprop()
    model.compile(loss='mse', optimizer=opt)
    return model   
    
    
    
def make_model_74_5():
    n_inputs = 2 + 2 + 6 + 6 #+ (34 + 34 + 34) #* 2
    
    board_input = Input(shape=(n_inputs,), name='board_input')
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')
    batch_normalization = BatchNormalization()(board_input)
    
    use_and_drop = concatenate([batch_normalization, action_input], axis=1, name='board_and_action')
    
    x = Dense(512, activation='relu')(use_and_drop)
    x = Dropout(0.2)(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.2)(x)
    #action_layer3 = Dense(32, activation='relu')(action_layer2)
    #action_layer4 = Dense(32, activation='relu')(action_layer3)
    #action_layer5 = Dense(32, activation='relu')(action_layer4)
    #action_layer6 = Dense(32, activation='relu')(action_layer5)
    
    
    
    
    
    x = Multiply()([action_input, Dense(34 * 3 * 2, activation='softmax')(x)])
    policy_output = Lambda(lambda x : x + 0.0000000000000001)(x)

    model = Model(inputs=[board_input, action_input], outputs=policy_output)
    opt = SGD(lr=0.000000001)
    #opt = SGD(lr=0.001)
    #opt = RMSprop()
    model.compile(loss='categorical_crossentropy', optimizer=opt)
    return model   
    
def make_model_79_5():
    n_inputs = 2 + 2 + 6 + 6 #+ (34 + 34 + 34) #* 2
    
    board_input = Input(shape=(n_inputs,), name='board_input')
    batch_normalization = BatchNormalization()(board_input)
    
    action_layer1 = Dense(512, activation='relu')(batch_normalization)
    #action_layer2 = Dense(32, activation='relu')(action_layer1)
    #action_layer3 = Dense(32, activation='relu')(action_layer2)
    #action_layer4 = Dense(32, activation='relu')(action_layer3)
    #action_layer5 = Dense(32, activation='relu')(action_layer4)
    #action_layer6 = Dense(32, activation='relu')(action_layer5)
    
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')
    
    
    #use_and_drop = concatenate([board_layer2, action_layer2], axis=1, name='board_and_action')
    policy_output = Multiply()([action_input, Dense(34 * 3 * 2, activation='softmax')(action_layer1)])
    

    model = Model(inputs=[board_input, action_input], outputs=policy_output)
    #opt = SGD(lr=0.000000001)
    opt = SGD(lr=0.00005)
    #opt = RMSprop()
    model.compile(loss='categorical_crossentropy', optimizer=opt)
    return model    
    
def make_model61_7():
    n_inputs = 2 + 2 + 6
    
    board_input = Input(shape=(n_inputs,), name='board_input')
    
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')

    value_output = Dense(1, activation='tanh', name='value_output')(board_input)
    
    hidden_layer_policy7 = Dense(34 * 3 * 2, activation='softmax', name='policy_output')(board_input)
    policy_output = Multiply()([action_input, hidden_layer_policy7])
    

    model = Model(inputs=[board_input, action_input], outputs=[value_output, policy_output])
    opt = SGD(lr=0.001)
    model.compile(loss=['mse', 'categorical_crossentropy'], optimizer=opt, loss_weights=[0.5, 1.0])
    
    return model
    
    
def make_model68_7():
    n_inputs = 2 + 2 + 6 + 6
    
    board_input = Input(shape=(n_inputs,), name='board_input')
    batch_normalization = BatchNormalization()(board_input)
    board_layer1 = Dense(256, activation='relu', name='board_layer1')(batch_normalization)
    board_layer2 = Dense(256, activation='relu', name='board_layer2')(board_layer1)
    board_layer3 = Dense(256, activation='relu', name='board_layer3')(board_layer2)
    
    action_layer1 = Dense(256, activation='relu')(batch_normalization)
    action_layer2 = Dense(256, activation='relu')(action_layer1)
    action_layer3 = Dense(256, activation='relu')(action_layer2)
    
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')
    
    value_output = Dense(1, activation='tanh', name='value_output')(board_layer3)
    
    hidden_layer_policy7 = Dense(34 * 3 * 2, activation='softmax', name='policy_output')(action_layer3)
    policy_output = Multiply()([action_input, hidden_layer_policy7])
    

    model = Model(inputs=[board_input, action_input], outputs=[value_output, policy_output])
    opt = SGD(lr=0.0001)
    model.compile(loss=['mse', 'categorical_crossentropy'], optimizer=opt, loss_weights=[0.5, 1.0])
    
    return model
    
    
def make_model71_1():
    n_inputs = 2 + 2 + 6 + 6 #+ (34 + 34 + 34) #* 2
    
    board_input = Input(shape=(n_inputs,), name='board_input')
    batch_normalization = BatchNormalization()(board_input)
    board_layer1 = Dense(256, activation='relu', name='board_layer1')(batch_normalization)
    board_layer2 = Dense(256, activation='relu', name='board_layer2')(board_layer1)
    board_layer3 = Dense(256, activation='relu', name='board_layer3')(board_layer2)
    
    action_layer1 = Dense(256, activation='relu')(batch_normalization)
    action_layer2 = Dense(256, activation='relu')(action_layer1)
    action_layer3 = Dense(256, activation='relu')(action_layer2)
    action_layer4 = Dense(256, activation='relu')(action_layer3)
    action_layer5 = Dense(256, activation='relu')(action_layer4)
    action_layer6 = Dense(256, activation='relu')(action_layer5)
    
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')

    value_output = Dense(1, activation='tanh', name='value_output')(board_layer3)
    
    hidden_layer_policy7 = Dense(34 * 3 * 2, activation='softmax', name='policy_output')(action_layer6)
    policy_output = Multiply()([action_input, hidden_layer_policy7])
    

    model = Model(inputs=[board_input, action_input], outputs=[value_output, policy_output])
    opt = SGD(lr=0.00001)
    model.compile(loss=['mse', 'categorical_crossentropy'], optimizer=opt, loss_weights=[0.5, 1.0])
    
    return model
    
    
def make_model72_8():
    n_inputs = 2 + 2 + 6 + 6
    
    board_input = Input(shape=(n_inputs,), name='board_input')
    batch_normalization = BatchNormalization()(board_input)
    board_layer1 = Dense(256, activation='tanh', name='board_layer1')(batch_normalization)
    board_layer2 = Dense(256, activation='tanh', name='board_layer2')(board_layer1)
    board_layer3 = Dense(256, activation='tanh', name='board_layer3')(board_layer2)
    
    action_layer1 = Dense(256, activation='tanh')(batch_normalization)
    action_layer2 = Dense(256, activation='tanh')(action_layer1)
    action_layer3 = Dense(256, activation='tanh')(action_layer2)
    action_layer4 = Dense(256, activation='tanh')(action_layer3)
    action_layer5 = Dense(256, activation='tanh')(action_layer4)
    action_layer6 = Dense(256, activation='tanh')(action_layer5)
    
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')

    value_output = Dense(1, activation='tanh', name='value_output')(board_layer3)

    hidden_layer_policy7 = Dense(34 * 3 * 2, activation='softmax', name='policy_output')(action_layer6)
    policy_output = Multiply()([action_input, hidden_layer_policy7])
    

    model = Model(inputs=[board_input, action_input], outputs=[value_output, policy_output])
    opt = SGD(lr=0.00001)
    model.compile(loss=['mse', 'categorical_crossentropy'], optimizer=opt, loss_weights=[0.5, 1.0])
    
    return model