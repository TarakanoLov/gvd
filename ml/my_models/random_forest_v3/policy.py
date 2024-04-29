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
#from contextualbandits.online import BootstrappedUCB, BootstrappedTS, \
 #           SeparateClassifiers, EpsilonGreedy, AdaptiveGreedy, ExploreFirst, \
  #          ActiveExplorer, SoftmaxExplorer
from copy import deepcopy

import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
import joblib
import lightgbm as lgb


class Critic:
    is_load = False
    
    def __init__(self):
        if not Critic.is_load:
            Critic.is_load = True
            Critic.bst = lgb.Booster(model_file='my_models/random_forest_v3/variants/v4_critic_0_137879.txt')
                
    def fit(self, x, y, *args, **kwargs):
        #Critic.model.fit(Critic.scaller.transform(x), y, *args, **kwargs)
        #Critic.model.fit(x, y, *args, **kwargs)
        #Critic.model.save_weights('my_models/critic_v1/variants/v1.h5')
        None
    
    def predict(self, x, *args, **kwargs):
        return Critic.bst.predict(x)