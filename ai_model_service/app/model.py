from pykeen.triples import TriplesFactory
import pandas as pd
import torch
import numpy as np

REAL_STATE_MODEL_PATH = 'app/data/trained_model.pkl'
DATASET_TRAIN_DATA_PATH = 'app/data/real_state_data_train.tsv.gz'


class RealStatePredictor:
    def __init__(self, model_path: str = REAL_STATE_MODEL_PATH):
        self.model = self.init_model(model_path)
        self.triples_factory = TriplesFactory.from_path(DATASET_TRAIN_DATA_PATH)
        self.same_as_relation_id = self.triples_factory.relation_to_id['http://www.w3.org/2002/07/owl#sameAs']
        print("RealStatePredictor initialized with model:", model_path)

    def init_model(self, model_path: str) -> torch.nn.Module:
        """
        Initialize the PyTorch model from the given model path.

        Args:
            model_path (str): The path to the PyTorch model file.

        Returns:
            torch.nn.Module: The initialized PyTorch model.
        """

        return torch.load(model_path, map_location="cpu", weights_only=False)
    
    def predict_best_similars(self, real_state_index: int, n: int = 10):
        """
        Predict the best n similar real estate properties to the given property.

        Args:
            real_state_index (int): The property index for which to find similar properties.
            n (int, optional): The number of similar properties to return. Defaults to 10.

        Returns:
            list[dict]: A list of dictionaries with 'index' and 'similarity'.
        """
        model_input = torch.tensor([(real_state_index, self.same_as_relation_id)])

        # Get similarity scores from the model
        scores = self.model.score_t(model_input).cpu().detach().numpy()[0]

        # Get top N most similar indices (excluding the first which is itself)
        similar_indices = np.argsort(scores)[1:n+1]

        # Construct a list of dictionaries
        similars = [{"index": int(idx), "similarity": float(scores[idx])} for idx in similar_indices]

        return similars

