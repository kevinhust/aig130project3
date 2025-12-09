from google.cloud import aiplatform
from sentence_transformers import SentenceTransformer


class Predictor:

    def __init__(self, project_id, region, endpoint_id):
        self.project_id = project_id
        self.region = region
        self.endpoint_id = endpoint_id
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=region)
        self.endpoint = aiplatform.Endpoint(endpoint_id)
        
        # Load local embedding model (must match training)
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')

    def predict(self, text_command):
        """
        Takes a raw text command, embeds it, and gets prediction from Vertex AI.
        """
        # 1. Embed text
        print(f"Embedding command: '{text_command}'")
        embeddings = self.embed_model.encode([text_command])
        # 2. Format for Vertex AI (list of instances)
        # Instance must match the feature names used in training.
        # Since we just passed raw embedding columns 'emb_0'...
        # we need to construct the instance dictionary or list properly.

        # AutoML Tabular usually expects a list of values if schema is not
        # provided, or a dict. Let's send a list of values (instances).
        # Create dict with keys matching the CSV header (emb_0, ...)
        instance = {
            f'emb_{i}': val for i, val in enumerate(embeddings[0])
        }

        # 3. Predict

        print("Sending request to Vertex AI Endpoint...")
        prediction = self.endpoint.predict(instances=[instance])

        # 4. Parse result
        # Prediction result structure depends on model type (classification).
        # Typically returns 'classes' and 'scores'.
        return prediction.predictions[0]

# usage example (commented out)
# predictor = Predictor('smart-home-mlops', 'us-central1', '1234567890')
# result = predictor.predict("Turn on the kitchen light")
# print(result)

