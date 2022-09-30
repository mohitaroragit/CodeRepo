from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\Pycharm\My First Project-086893815f2b.json"
client=bigquery.Client(project='resonant-tower-274312')
table_id='resonant-tower-274312.my_first_datset.BigQ_Table'
job_config=bigquery.QueryJobConfig(destination=table_id)
sql="""
select Industry_aggregation_NZSIOC,Industry_code_NZSIOC,max(Value) as Value from `resonant-tower-274312.my_first_datset.Enterprise`
group by Industry_aggregation_NZSIOC,Industry_code_NZSIOC
"""
query_ret=client.query(sql,job_config=job_config)
query_ret.result()
print("Query Result loaded to the table {}".format(table_id))