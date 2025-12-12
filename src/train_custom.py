import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
import sys

# Add src to python path to import config
sys.path.append(os.path.abspath("src"))
import config

def train_local():
    print("🚀 Starting Local Training...")
    
    # 1. Load Data
    data_path = "dataset_augmented.csv" 
    if not os.path.exists(data_path):
        data_path = "dataset.csv" # Fallback
        
    print(f"📂 Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"   Rows: {len(df)}")
    
    # 2. Embeddings
    import time
    print("🧠 Generating embeddings (this may take a moment)...")
    
    embedder = None
    for attempt in range(5):
        try:
            embedder = SentenceTransformer('all-MiniLM-L6-v2')
            break
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed to load HF model: {e}")
            time.sleep(10 * (attempt + 1))
            
    if embedder is None:
        raise RuntimeError("Failed to download HF model after 5 attempts")
    X = embedder.encode(df['Sentence'].tolist())
    y = df['Category']
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train Model
    print("🌲 Training Random Forest Classifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # 5. Evaluate
    print("📊 Evaluation on Test Set:")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # 6. Save Model
    artifact_dir = "model_artifacts"
    os.makedirs(artifact_dir, exist_ok=True)
    model_path = os.path.join(artifact_dir, "model.joblib")
    
    joblib.dump(clf, model_path)
    print(f"💾 Model saved to {model_path}")
    
    # Save the label encoder classes if needed, or just relying on model's classes_
    print(f"   Classes: {clf.classes_}")

if __name__ == "__main__":
    train_local()
