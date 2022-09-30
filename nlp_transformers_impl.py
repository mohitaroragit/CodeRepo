from transformers import pipeline
query=pipeline("question-answering")
query(question="Who is Mohit ?",
       context="My name is Mohit and I work as Freelancer",)
print(query)