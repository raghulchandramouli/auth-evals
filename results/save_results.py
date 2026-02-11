import os
import pandas as pd
from datetime import datetime

def save_results(
    model_name   : str,
    dataset_name : str,
    metrics      : dict,
    transform    : str = 'clean',
    output_dir   : str = 'results/opensource',
):
    
    """
    This function is used to save the results of the evaluation.
    
    Args:
        model_name   : Name of the artifact used
        dataset_name : Name of the dataset used to test evaluation.
        metrics      : A dictionary containing the metrics of the evaluation.
        transform    : transformation applied to the Images.
        output_dir   : Directory to save the results.
    
    Returns:
            f1, accuracy, auc, recall
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"{dataset_name}_results.csv")
    
    row = {
        'model'    : model_name,
        'dataset'  : dataset_name,
        'accuracy' : metrics.get('accuracy'),
        'f1'       : metrics.get('f1'),
        'auc'      : metrics.get('auc'),
        'transform': transform,
        'timestamp': datetime.now().strftime('%y-%m-%d %H-%M-%S')
    }
    
    df = pd.DataFrame([row])
    
    # Append if exist
    if os.path.exists(output_path):
        df.to_csv(output_path, mode='a', header=False, index=False)
    else:
        df.to_csv(output_path, index=False)
        
    print(f"Results saved to {output_path}")
