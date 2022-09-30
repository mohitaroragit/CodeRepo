import spacy
nlp=spacy.load("en_core_web_lg")
w1="weather"
w2="rainy"
w1=nlp.vocab[w1]
w2=nlp.vocab[w2]
print(w1.similarity(w2))
s1=nlp("I do not know whether I want you ")
s2=nlp("I don't know the weather for it. I warned you")
s3=nlp("Today is an awful sunny day and I told you so")
print(s1.similarity(s2))
print(s1.similarity(s3))
print(s2.similarity(s3))