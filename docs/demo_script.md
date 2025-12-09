# Demo Script (15 Minutes)

## **Part 1: The Pipeline Run (3 mins)**
1.  **Show Code**: Open `src/embed.py` and `ml-pipeline.yml`. Explain: "Here is where we create embeddings and trigger the cloud job."
2.  **Trigger Action**: Make a small change (e.g., add a comment) to `README.md` and push to GitHub.
3.  **Show GitHub**: Go to 'Actions' tab. Show the workflow starting. "The pipeline is now building the Docker image and authenticating with GCP."

## **Part 2: The Training (Skip/Show Console) (2 mins)**
1.  **Vertex Console**: Switch to GCP Console > Vertex AI > Training.
2.  **Show Job**: "Here is the job triggered by our pipeline. Since it takes ~1 hour, I have a pre-trained model deployed here."

## **Part 3: Live Prediction (5 mins) - THE WOW FACTOR**
1.  **Launch App**: Run `streamlit run src/app.py` locally.
2.  **Scenario 1**: Type "Turn on the kitchen lights".
    - *Result*: `lights_kitchen_on_now` (99%).
3.  **Scenario 2**: Type "Set the thermostat to 70 degrees".
    - *Result*: `temperature_thermostat_set_now`.
4.  **Scenario 3 (Complex)**: Type "I need the living room dark immediately".
    - *Result*: `lights_livingroom_off_now`. (Shows semantic understanding!)

## **Part 4: Monitoring & Conclusion (3 mins)**
1.  **Show Endpoint**: Go to Vertex AI > Endpoints. Show the request count spike from your demo.
2.  **Reflection**: "We successfully automated the path from raw CSV to a deployed semantic classifier using less than $2 in resources."
