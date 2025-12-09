# Evaluation Metrics & Baselines

| Metric | Baseline (Rule-based) | Target (AutoML) | Description |
| :--- | :--- | :--- | :--- |
| **Accuracy** | 60% | > 85% | Percentage of correct 'Intent' predictions. |
| **F1-Score (Macro)** | 0.55 | > 0.80 | Balanced metric handling class imbalance. |
| **Latency** | N/A | < 100ms | Inference time per command. |

---

## Metric Justification
- **Macro F1**: The dataset has imbalanced classes (e.g., 'lights' is 16%, others are smaller). Accuracy can be misleading. Macro F1 ensures we perform well on minority classes too.
