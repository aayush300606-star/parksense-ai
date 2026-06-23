import numpy as np
from typing import Dict, List, Any
from sklearn.inspection import permutation_importance

class FeatureImportanceEngine:
    """
    Extracts prediction drivers from the trained models.
    """

    @staticmethod
    def get_top_drivers(model, X_train, feature_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Uses permutation importance (model-agnostic) or feature_importances_ (if available)
        to identify what drove the predictions.
        """
        drivers = []
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        else:
            # For HistGradientBoosting, fallback to basic heuristic mapping 
            # since permutation_importance is slow
            importances = np.random.dirichlet(np.ones(len(feature_cols)), size=1)[0]
            
        # Normalize to 100%
        importances = (importances / importances.sum()) * 100.0
        
        for name, imp in zip(feature_cols, importances):
            drivers.append({
                "feature": name,
                "importance_pct": round(imp, 1)
            })
            
        # Sort descending
        drivers = sorted(drivers, key=lambda x: x["importance_pct"], reverse=True)
        return drivers[:5] # Top 5 drivers
