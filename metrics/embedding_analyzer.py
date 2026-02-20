"""
This is a place in which is used to handle PCA, ICA, Embedding Distance

Usage:
    analyzer = EmbeddingAnalyzer()
    out = analyzer.analyze(embeddings)
"""

from __future__ import annotations
from typing import Dict, Mapping, Sequence

import numpy as np
from sklearn.decomposition import FastICA, PCA

class EmbeddingAnalyzer:
    """
    Standalone helper for representation analysis across models.
    
    Input format:
    {
        'model_a': [embedding_1, embedding_2, ...],
        'model_b': [embedding_1, embedding_2, ...],
    }
    """
    
    def __init__(self, n_components: int = 2, random_state: int = 42, ica_max_iter: int = 1000):
        self.n_components = n_components
        self.random_state = random_state
        self.ica_max_iter = ica_max_iter
        
    @staticmethod
    def _to_2d_array(values: Sequence[Sequence[float]]):
        arr = np.asarray(values, dtype=np.float32)
        
        if arr.ndim != 2:
            raise ValueError(f"Expected 2D array, got {arr.ndim}D array.")
        
        if arr.shape[0] == 0 or arr.shape[1] == 0:
            rause ValueError(f'Embeddings must be non-empty')
        
        return arr
    
    def _centroids(self, embeddings_by_model: Mapping[str, Sequence[Sequence[float]]]) -> Dict[str, np.ndarray]:
        centroids: Dict[str, np.ndarray] = {}
        
        for model_name, embeds in embeddings_by_model.items():
            arr = self._to_2d_array(embeds)
            centroids[model_name] = np.mean(axis=0)
        
        if len(centroids) < 2:
            raise ValueError('Need at least two models to compute distances')
        return centroids
    
    @staticmethod
    def _cosine_distance(
        x : np.ndarray,
        b : np.ndarray
    ) -> float:
        
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(1.0 - (np.dot(a, b) / denom)) 
         
         
     def pairwise_distance(self,
                           embeddings_by_model: Mapping[str, Sequence[Sequence[float]]]) -> list[dict]:
         
         centroids = self._centroids(embeddings_by_model)
         model_names = list(centroids.keys())    
         
         rows = []
         for i in range(len(model_names)):
             for j in range(i + 1, len(model_names)):
                 a_name = model_names[i]
                 b_name = model_names[j]
                 a = centroids[a_name]
                 b = centroids[b_name]
                 rows.append(
                     {
                         'model_a' : a_name,
                         'model_b' : b_name,
                         'euclidean' : float(np.linalg.norm(a - b)),
                         'cosine'   : self._cosine_distance(a, b)
                     }
                 )
                 
         return rows
     
     def _Project(self, embeddings_by_model: Mapping[str, Sequence[Sequence[float]]]
                  method: str) -> dict:
         
         centroids = self._centroids(embeddings_by_model)
         model_names = list(centroids.keys())
         
         matrix = np.stack([centroids[name] for name in model_names], axis = 0)
         n_models, emb_dim = matrix.shape
         n_components = min(self.n_components, n_models, emb_dim)
         
         if n_components < 1:
             return {
                 'components' : 0,
                 'points'     : []
             }
             
         if method == 'pca':
             projector = PCA(n_components=n_components, random_state = self.random_state)
             projected = projector.fit_transform(matrix)
             
             return {
                 'components' : int(n_components),
                 'explained_variance_ratio' : [float(v) for v in projector.explained_variance_ratio_],
                 'points' : [
                    {
                        'model' : model_names[i], 
                        'values' : [float(v) for v in projected[i]]
                    }
                    
                     for i in range(n_models)
                ],
             }
             
         if method == 'ica':
             projector = FastICA(
                 n_components = n_components,
                 random_state = self.random_state,
                 max_iter = self.ica_max_iter
             )
             
             projector = projector.fit_transform(matrix)
             return {
                 'components' : int(n_components),
                 'points' : [
                     {"model" : model_names[i], "values": [float(x) for x in projected[i]]}
                     for i in range(n_models)
                 ],
             }
             
          raise ValueError(f"Unknown projection method: {method}")
      
      def pca(self, embeddings_by_model : Mapping[str, Sequence[Sequence[float]]]) -> dict:
          return self._Project(embeddings_by_model, method='pca')
      
      def ica(self, embeddings_by_model : Mapping[str, Sequence[Sequence[float]]]) -> dict:
          return self._Project(embeddings_by_model, method='ica')

      def analyze(self, embeddings_by_model : Mapping[str, Sequence[Sequence[float]]]) -> dict:
          return {
              'pairwise_distances' : self.pairwise_distance(embeddings_by_model),
              'pca' : self.pca(embeddings_by_model),
              'ica' : self.ica(embeddings_by_model),
          }
