from datasets import Dataset, load_dataset
from huggingface_hub import login

# Login using your token
login(token='')

# Now you can load the gated dataset
ds = load_dataset("uonlp/CulturaX", "zh", split="train", streaming=True)
