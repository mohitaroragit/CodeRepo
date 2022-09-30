from datasets import load_dataset
from transformers import AutoTokenizer

emotion_dataset=load_dataset("emotion")
print(emotion_dataset["train"][0])
emotion_df=emotion_dataset["train"].to_pandas()
print(emotion_df.head())
features=emotion_dataset["train"].features
print(features)
print(features["label"].int2str(0))
id2label={idx:features["label"].int2str(idx) for idx in range(6)}
print(id2label)
label2id={v:k for k,v in id2label.items()}
print(label2id)
model_ckpt="microsoft/MiniLM-L12-H384-uncased"
tokenizer=AutoTokenizer.from_pretrained(model_ckpt)