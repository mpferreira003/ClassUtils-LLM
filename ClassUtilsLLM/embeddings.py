import numpy as np
from enum import Enum

def L1_norm(embeddings):
    """
    This function is responsible for performing 'L1' normalization on embeddings.
    
    Args:
        embeddings:np.ndarray - The input embeddings to be normalized.
    
    Returns:
        :np.ndarray - The L1-normalized embeddings.
    """
    norm = np.abs(embeddings).sum(axis=1)[:, None]
    return embeddings / norm


def L2_norm(embeddings):
    """
    This function is responsible for performing 'L2' normalization on embeddings
    
    Args:
        embeddings:np.ndarray - The input embeddings to be normalized.
    
    Returns:
        :np.ndarray - The L1-normalized embeddings.
    """
    norm = np.sqrt((embeddings**2).sum(axis=1))[:,None]
    return embeddings / norm


class normalizers(Enum):
    L1 = 1
    L2 = 2

def norm(embeddings,type=normalizers.L2):
    """
    Main function for normalization
    
    Args:
        embeddings:np.ndarray - embeddings to normalize
        type:normalizers [default = normalizers.L2] - type of normalization
    
    Returns:
        :np.ndarray - normalized embeddings
    """
    if normalizers.L1==type:
        return L1_norm(embeddings)
    elif normalizers.L2==type:
        return L2_norm(embeddings)
    else:
        raise ValueError("normalizer's type is invalid")

def remove_duplicates(embeddings,return_index=False):
    """
    A function that removes repeated embeddings. Istead of using this 
    function, you can apply a text comparison between all data to remove 
    duplicates.
    
    Args:
        embeddings:np.ndarray - embeddings of your text dataset
        return_index:bool [default = False] - return the indexes that you must
            keep in the dataset to remove the duplicates
    Returns:
        embeddings_cleared:np.array - embeddings without duplicates (only if return_index==False)
        indexes:int - indexes you must keep to remove duplicates (only if return_index==True)
    """
    if return_index:
        return np.unique(embeddings,axis=0,return_index=return_index)[1]
    else:
        return np.unique(embeddings,axis=0,return_index=True)