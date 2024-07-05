from bertPredictor import BertPredictor
from mlkmeans import MustLinkKMeans
import numpy as np
from enum import Enum

def run_bertPred(trainX,trainY,embeddings,**kwargs):
    pred = BertPredictor(num_labels=kwargs['num_labels'])
    pred.compile()
    pred.fit(trainX,trainY,epochs=kwargs['epochs'])
    return pred.predict(embeddings)
    
def run_mlPred(trainX_idxs,trainY,embeddings,**kwargs):
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


def predictor(amostrasXidx,amostrasY,embeddings,method=methods.PURE_BERT,**kwargs):
    if method==methods.PURE_BERT:
        return run_bertPred([embeddings[idx] for idx in amostrasXidx],
                     amostrasY,embeddings,**kwargs)
    elif method==methods.MLKMEANS:
        return run_mlPred(amostrasXidx,amostrasY,embeddings,**kwargs)
    else:
        raise ValueError("predictor's method is invalid")