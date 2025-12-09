import streamlit as st
import os
from predict import Predictor

# Configuration
# Ideally these come from env vars or config file
PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'smart-home-mlops')
REGION = os.environ.get('GCP_REGION', 'us-central1')
ENDPOINT_ID = os.environ.get('VERTEX_ENDPOINT_ID', '')  # User sets this

st.title("🏠 Smart Home Command Intent Classifier")
st.markdown("""
This demo uses **HuggingFace** for text embeddings
and **Google Cloud Vertex AI** for intent classification.
""")


# Sidebar config
st.sidebar.header("Configuration")
project_id_input = st.sidebar.text_input("GCP Project ID", value=PROJECT_ID)
region_input = st.sidebar.text_input("GCP Region", value=REGION)
endpoint_id_input = st.sidebar.text_input(
    "Vertex Endpoint ID", value=ENDPOINT_ID
)

if not endpoint_id_input:
    st.warning("Please enter a Vertex AI Endpoint ID in the sidebar.")
else:
    # Initialize Predictor
    try:
        predictor = Predictor(project_id_input, region_input, endpoint_id_input)
        st.success("Connected to Vertex AI Endpoint!")
    except Exception as e:
        st.error(f"Failed to connect: {e}")
        predictor = None

    # Input Area
    command = st.text_input(
        "Enter a voice command:",
        placeholder="e.g., Turn on the kitchen lights now"
    )


    if st.button("Classify") and command and predictor:

        with st.spinner("Processing..."):
            try:
                # Get prediction
                result = predictor.predict(command)

                # Display Results
                st.subheader("Prediction Result")

                # Handling AutoML Tabular Classification response format
                # Usually: {'classes': ['class1'], 'scores': [0.9]}
                if 'classes' in result and 'scores' in result:
                    classes = result['classes']
                    scores = result['scores']

                    # Find top class
                    max_score_idx = scores.index(max(scores))
                    top_class = classes[max_score_idx]
                    top_score = scores[max_score_idx]

                    st.metric(
                        "Predicted Intent",
                        top_class,
                        f"{top_score:.2%}"
                    )

                    # Breakdown
                    parts = top_class.split('_')
                    if len(parts) >= 4:
                        cols = st.columns(4)
                        cols[0].metric("Category", parts[0])
                        cols[1].metric("Subcategory", parts[1])
                        cols[2].metric("Action", parts[2])
                        cols[3].metric("Time", parts[3])

                    # Show all confidences
                    with st.expander("Full Confidence Scores"):
                        score_dict = dict(zip(classes, scores))
                        st.bar_chart(score_dict)
                else:
                    st.write(result)

            except Exception as e:
                st.error(f"Prediction Error: {e}")

st.markdown("---")
st.caption("Built for AIG130 Project 3")

