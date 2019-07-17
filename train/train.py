# %%
import tensorflow as tf
from tensorflow import keras
import numpy
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

print(tf.__version__)

# %%
train_df = pd.read_csv('CORN.csv', sep=',')

print(train_df.head())