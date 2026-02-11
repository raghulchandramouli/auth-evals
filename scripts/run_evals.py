# scripts/run_evals.py
"""
This script is used to run the evaluations for the models.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from PIL import Image
from metrics.classification import compute_metrics
from results.save_results import save_results
from inferencers.dummy_inferencer import DummyInferencer
def evaluate(inferencer, metadata_csv):
    """
    
    This is used to evaluate the model

    Args:
        inferencer : this acts as a wrapper for model inference.
        metadata_csv : The metadata csv file containing the images and their labels.
    Returns:
        dict: A dictionary containing the metrics.
    """
    
    df = pd.read_csv(metadata_csv)
    
    y_true = []
    y_pred = []
    y_scores = []
    
    
    for _, row in df.iterrows():
        image = Image.open(row['image_path'])
        
        output = inferencer.predict(image)
        
        fake_prob = output['fake_prob']
        pred_label = 1 if fake_prob > 0.5 else 0
        
        y_true.append(row['label'])
        y_pred.append(pred_label)
        y_scores.append(fake_prob)
        
    
    return compute_metrics(y_true, y_pred, y_scores)

def main():
    
    model_name = 'dummy_model'
    dataset_name = 'dummy'
    
    metrics = evaluate(inferencer, metadata_csv)
    
    print(metrics)
    
    save_results(
        model_name = model_name,
        dataset_name = dataset_name,
        metrics = metrics,
        transform = 'clean'
    )