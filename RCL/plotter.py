from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
import numpy as np


def plot(X,y,ax,title,gt=None,score=adjusted_rand_score):
  """
  Function to plot the embeddings
  
  Args:
    X: np.ndarray - embeddings
    y: np.ndarray - true labels
    ax: matplotlib axes - plot axes
    title: str - plot title
    gt: np.ndarray [default=None] - ground truth labels
    score: callable [default=adjusted_rand_score] - metric to calculate score
  """ 
  ax.set_title(title)
  if gt is not None:
    score = score(gt,y)
    ax.annotate('{:.2}'.format(score), xy=(0.8, 1), xytext=(0, 3),
              xycoords='axes fraction', textcoords='offset points',
              ha='center', va='bottom')
  for label in np.unique(y):
    idxs = np.where(label==y)
    ax.scatter(X[idxs,0],X[idxs,1],alpha=0.5)