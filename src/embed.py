import pandas as pd
from sentence_transformers import SentenceTransformer
from google.cloud import storage
import argparse


def process_data(input_file, bucket_name, destination_blob_name):
    """
    Reads CSV, generates embeddings, creates a combined target,
    and uploads to GCS.
    """
    print(f"Loading data from {input_file}...")

    # Load dataset
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return

    # 1. Feature Engineering: Embeddings
    print("Generating embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['Sentence'].tolist())

    # Create DataFrame from embeddings
    embedding_cols = [f'emb_{i}' for i in range(embeddings.shape[1])]
    df_embeddings = pd.DataFrame(embeddings, columns=embedding_cols)

    # 2. Target Engineering: Combine columns for multi-class classification
    # Combining Category, Subcategory, Action, Time into a single string
    # Handling potential missing values by filling with 'none'
    df_filled = df.fillna('none')
    df_embeddings['target_intent'] = (
        df_filled['Category'].astype(str) + "_" +
        df_filled['Subcategory'].astype(str) + "_" +
        df_filled['Action'].astype(str) + "_" +
        df_filled['Time'].astype(str)
    )


    # 3. Create final AutoML-ready CSV
    # AutoML Tabular expects target column and feature columns
    final_df = df_embeddings

    output_filename = 'training_data.csv'
    final_df.to_csv(output_filename, index=False)

    print(f"Processed data saved locally to {output_filename}")

    # 4. Upload to GCS
    if bucket_name:
        print(f"Uploading to GCS bucket: {bucket_name}...")
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(output_filename)
        print(f"File uploaded to gs://{bucket_name}/{destination_blob_name}")
    else:
        print("No bucket provided, skipping upload.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_file', type=str, default='data/dataset.csv',
        help='Path to input CSV'
    )
    parser.add_argument(
        '--bucket_name', type=str, help='GCS bucket name for output'
    )
    parser.add_argument(
        '--destination_blob_name', type=str,
        default='data/final_training_data.csv',
        help='GCS path for output'
    )
    args = parser.parse_args()

    process_data(
        args.input_file, args.bucket_name, args.destination_blob_name
    )
