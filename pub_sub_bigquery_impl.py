import json
from google.cloud import bigquery
from google.cloud import pubsub_v1
import base64
import os,time,datetime
import utils
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='D:\Pycharm\GCP\key-bigquery-practice-sample-f06cc09971f9.json'
PROJECT_ID='bigquery-practice-sample'
PUB_SUB_TOPIC='pub-sub-topic'
NUM_RETRIES=3
def fqrn(resource_type,project,resource):
    return "projects/{}/{}/{}".format(project,resource_type,resource)
def create_subscription(client,project_name,sub_name):
    print("Using PubSub topic : %s" %PUB_SUB_TOPIC)
    name=get_full_subscription_name(project_name,sub_name)
    body={'topic':PUB_SUB_TOPIC}
    subscription=client.projects().subscriptions().create(
        name=name,body=body).execute(num_retries=NUM_RETRIES)
    print('Subscription {} was created. '.format(subscription['name']))
def get_full_subscription_name(project,subscription):
    return fqrn('subscriptions',project,subscription)
def pull_messages(client,project_name,sub_name):
    BATCH_SIZE=50
    tweets=[]
    subscription=get_full_subscription_name(project_name,sub_name)
    body={
        'returnImmediately':False,
        'maxMessages':'BATACH_SIZE'
    }
    try:
        resp=client.projects().subscriptions().pull(
            subscription=subscription,body=body).execute(
            num_retries=NUM_RETRIES
        )
    except  Exception as e:
        print("Exception : %s" %e)
        time.sleep(0.5)
        return
    receivedMessages=resp.get('recievedMessages')
    if receivedMessages is not None:
        ack_ids=[]
        for receivedMessage in receivedMessages:
            message=receivedMessage.get('message')
            if message:
                tweets.append(
                    base64.urlsafe_b64decode(str(message.get('data'))))
        ack_body={'ackIds':ack_ids}
        client.projects().subscriptions().acknowledge(
            subscription=subscription,body=ack_body).execute(
            num_retries=NUM_RETRIES
        )
    return tweets
def write_to_bq(pubsub,sub_name,bigquery):
    tweets=[]
    CHUNK=50
    WAIT=2
    tweet=None
    mtweet=None
    count=0
    count_max=50000
    while count < count_max:
        while len(tweets) < CHUNK:
            twmessages=pull_messages(pubsub,PROJECT_ID,sub_name)
            if twmessages:
                for res in twmessages:
                    try:
                        tweet=json.loads(res)
                    except Exception as e:
                        print(e)
                    mtweet=utils.cleanup(tweet)
                    if 'delete' in mtweet:
                        continue
                    if 'limit' in mtweet:
                        continue
                    tweets.append(mtweet)
            else:
                print('Sleeping')
                time.sleep(WAIT)
        response=utils.bq_data_insert(bigquery,PROJECT_ID,os.environ['BQ_DATASET'],
                                      os.environ['BQ_TABLES'],tweets)
        tweets=[]
        count+=1
        if count%25==0:
            print('Processing count : %s of %s at %s  : %s' %
                  (count,count_max,datetime.datetime.now(),response))

if __name__=="__main__":
    topic_info=PUB_SUB_TOPIC.split('/')
    topic_name=topic_info[-1]
    sub_name="tweets-%s" %topic_name
    print("Starting to write to BigQuery...")
    credentials=utils.get_credentials()
    bigquery=utils.create_bigquery_client(credentials)
    pubsub=utils.create_pubsub_client(credentials)
    try:
        subscription=create_subscription(pubsub,PROJECT_ID,sub_name)
    except Exception as e:
        print(e)
    write_to_bq(pubsub,sub_name,bigquery)
    print('Exited write loop')

