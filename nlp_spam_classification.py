import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
df=pd.read_csv('D:\Pycharm\Spam Email raw text for NLP.csv')
print(df['CATEGORY'].value_counts())
tokenizer=nltk.RegexpTokenizer(r"\w+")
test_message="Hey,How is it going ?<HTML> randomly"
test_message_tokenize=tokenizer.tokenize(test_message)
#print(test_message_tokenize)
test_message_lowercase=[t.lower() for t in test_message_tokenize]
#print(test_message_lowercase)
lematizer=WordNetLemmatizer()
test_message_lematize_tokens=[lematizer.lemmatize(t) for t in test_message_lowercase]
#print(test_message_lematize_tokens)
stopwords=stopwords.words('english')
test_message_useful_tokens=[t for t in test_message_lematize_tokens if t not  in stopwords]
#print(test_message_useful_tokens)
def message_to_token_list(s):
    tokens=tokenizer.tokenize(s)
    lowercase_tokens=[t.lower() for t in tokens]
    lematize_tokens=[lematizer.lemmatize(t) for t in lowercase_tokens]
    useful_tokens=[ t for t in lematize_tokens if t not in stopwords]
    return useful_tokens
print(message_to_token_list(test_message))
df=df.sample(frac=1,random_state=1)
df=df.reset_index(drop=True)
split_index=int(len(df) * 0.8)
train_df,test_df=df[:split_index],df[split_index:]
train_df=train_df.reset_index(drop=True)
test_df=test_df.reset_index(drop=True)
#print(train_df,test_df)
token_counter={}
for message in train_df['MESSAGE']:
    message_as_token_list=message_to_token_list(message)
    for token in message_as_token_list:
        if token in token_counter:
            token_counter[token]+=1
        else:
            token_counter[token]=1
len(token_counter)
print(token_counter)
def keep_token(processed_token,threshold):
    if processed_token not in token_counter:
        return False
    else:
        return token_counter[processed_token] > threshold
print(keep_token('random',50))
features=set()
for token in token_counter:
    if keep_token(token,10000):
        features.add(token)
print(features)
features=list(features)
print(features)
token_to_index_mapping={t:i for t,i in zip(features,range(len(features)))}
print(token_to_index_mapping)
print(message_to_token_list('3d  b  <br> . com bad font font com randoms'))
def message_to_count_vector(message):
    count_vector=np.zeros(len(features))
    processed_list_of_tokens=message_to_token_list(message)
    for token in processed_list_of_tokens:
        if token not in features:
            continue
        index=token_to_index_mapping[token]
        count_vector[index]+=1
    return count_vector
print(message_to_count_vector('3d  b  <br> . com bad font font com randoms'))
print(message_to_count_vector(train_df['MESSAGE'].iloc[65]))
print(train_df.iloc[3])
def df_to_X_y(dff):
    y=dff['CATEGORY'].to_numpy().astype(int)
    message_col=dff['MESSAGE']
    count_vectors=[]
    for message in message_col:
        count_vector=message_to_count_vector(message)
        count_vectors.append(count_vector)
    X=np.array(count_vectors).astype(int)
    return X,y
X_train,y_train=df_to_X_y(train_df)
X_test,y_test=df_to_X_y(test_df)
print(X_train.shape,y_train.shape,X_test.shape,y_test.shape)
scaler=MinMaxScaler().fit(X_train)
X_train,X_test=scaler.transform(X_train),scaler.transform(X_test)
print(X_train)
lr=LogisticRegression().fit(X_train.y_train)
print(classification_report(y_test,lr.predict(X_test)))
