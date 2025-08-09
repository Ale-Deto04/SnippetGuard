import torch
import warnings
from transformers import AutoTokenizer, RobertaForSequenceClassification
from scipy.special import expit
from config import MODEL_PATH, THRESHOLD, LABELS

warnings.filterwarnings("ignore", message=".*encoder_attention_mask.*", category=FutureWarning) # encoder_attention_mask deprecated

# Load model, tokenizer and labels
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = RobertaForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# Use GPU if available
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#model.to(device)

# Default: use CPU
device = torch.device("cpu")
model.to(device)

# Classifies a single snippet (string) of code
def classify_snippet(snippet):
    inputs = tokenizer(snippet, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = expit(logits.cpu().numpy())[0]
        preds = [LABELS[i] for i, p in enumerate(probs) if p >= THRESHOLD]

    vuln = list(zip(LABELS, probs))

    return preds, vuln