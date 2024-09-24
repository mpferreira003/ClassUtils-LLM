from .bertPredictor import BertPredictor
from .mlkmeans import MustLinkKMeans
import numpy as np
from enum import Enum

def run_bertPred(trainX,trainY,all_docs,**kwargs):
    """
    Call a BertPredictor, compile, fit it and predict
    Args:
        trainX:list[str] - train data texts
        trainY:list[int] - train data labels
        all_docs:list[str] - all the data text
        kwargs:
            --> it needs 'num_labels' (int)
            --> it needs 'epochs' (int)
    
    Returns:
        :list[int] - predicted labels 
    """
    pred = BertPredictor(num_labels=kwargs['num_labels'])
    pred.compile()
    pred.fit(trainX,trainY,epochs=kwargs['epochs'])
    return pred.predict(all_docs)
    
def run_mlPred(trainX_idxs,trainY,embeddings,**kwargs):
    """
    Call a MustLink, fit it and predict
    Args:
        trainX_idxs:list[int] - indices of train embeddings
        trainY:list[int] - train data labels
        embeddings:np.ndarray - all the data
        kwargs:
            --> it needs 'max_iters' (int)
            --> it needs 'tol' (float)
    
    Returns:
        :list[int] - predicted labels 
    """
    ml = []
    uniques = np.unique(trainY)
    for label in uniques:
        indices = np.where(trainY==label)
        mlg = [[indices[i],indices[i+1]] for i in range(len(indices)-1)]
        ml.extend([trainX_idxs[idx_internal] for idx_internal in mlg])
    mlkmeans = MustLinkKMeans(len(uniques),
                   max_iters=kwargs['max_iters'],
                   tol=kwargs['tol'],)
    mlkmeans.fit(embeddings,ml=ml)
    return mlkmeans.labels_

class methods(Enum):
    PURE_BERT = 0
    MLKMEANS = 1


def predictor(amostrasXidx,amostrasY,embeddings,all_docs,method=methods.PURE_BERT,**kwargs):
    """
    Main funtion for prediction
    Args:
        amostrasXidx:list[int] - indices of embeddings for training
        amostrasY:list[int] - labels of training
        embeddings - all the data
        method:methods [default = methods.PURE_BERT] - method to be used
        kwargs: depends of choosed method
    Returns:
        :list[int] - the predicted labels
    """
    if method==methods.PURE_BERT:
        return run_bertPred([all_docs[idx] for idx in amostrasXidx],amostrasY,all_docs,**kwargs)
    elif method==methods.MLKMEANS:
        return run_mlPred(amostrasXidx,amostrasY,embeddings,**kwargs)
    else:
        raise ValueError("predictor's method is invalid")