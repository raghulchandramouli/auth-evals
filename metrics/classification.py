from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

def compute_metrics(y_true, y_pred, y_scores):
    
    return {
        'accuracy' : accuracy_score(y_true, y_pred),
        'f1' : f1_score(y_true, y_pred),
        'auc' : roc_auc_score(y_true, y_scores)
    }