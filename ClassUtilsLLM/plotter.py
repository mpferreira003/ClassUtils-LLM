from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
import numpy as np


def plot(X,y=None,title=None,ax=None,gt=None,score=adjusted_rand_score):
  """
  Function to plot the embeddings
  
  Args:
    X: np.ndarray - embeddings
    y: np.ndarray [default=None] - true labels. By default, it will be 0
      for every embedding.
    title: str [default=None] - plot title. By default, it will not displayed.
    ax: matplotlib axes [default=None] - plot axes. If not specified, 
      it will use matplotlib default plot.
    gt: np.ndarray [default=None] - ground truth labels
    score: callable [default=adjusted_rand_score] - metric to calculate score
  """ 
  if y is None:
    y = np.zeros_like(X[:,0])  # set default labels to 0 for all embeddings
  
  if ax is not None:
    if title is not None:
      ax.set_title(title)
    if gt is not None:
      score = score(gt,y)
      ax.annotate('{:.2}'.format(score), xy=(0.8, 1), xytext=(0, 3),
                xycoords='axes fraction', textcoords='offset points',
                ha='center', va='bottom')
    for label in np.unique(y):
      idxs = np.where(label==y)
      ax.scatter(X[idxs,0],X[idxs,1],alpha=0.5)
  else:
    if title is not None:
      plt.title(title)
    if gt is not None:
      score = score(gt,y)
      plt.annotate('{:.2}'.format(score), xy=(0.8, 1), xytext=(0, 3),
                xycoords='axes fraction', textcoords='offset points',
                ha='center', va='bottom')
    for label in np.unique(y):
      idxs = np.where(label==y)
      plt.scatter(X[idxs,0],X[idxs,1],alpha=0.5)