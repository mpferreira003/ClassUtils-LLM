import numpy as np
from enum import Enum

def L1_norm(embeddings):
    """
    This function is responsible for performing 'L1' normalization on embeddings.
    
    Args:
    embeddings (np.ndarray): The input embeddings to be normalized.
    
    Returns:
    np.ndarray: The L1-normalized embeddings.
    """
    norm = np.abs(embeddings).sum(axis=1)[:, None]
    return embeddings / norm


def L2_norm(embeddings):
    """
    This function is responsible for performing 'L2' normalization on embeddings
    
    Args:
    embeddings - (np.ndarray): The input embeddings to be normalized.
    
    Returns:
    np.ndarray: The L1-normalized embeddings.
    """
    norm = np.sqrt((embeddings**2).sum(axis=1))[:,None]
    return embeddings / norm


class normalizers(Enum):
    L1 = 1
    L2 = 2

def norm(embeddings,type=normalizers.L2):
    if normalizers.L1==type:
        return L1_norm(embeddings)
    elif normalizers.L2==type:
        return L2_norm(embeddings)
    else:
        raise ValueError("normalizer's type is invalid")