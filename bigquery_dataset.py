from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\Pycharm\GCP\key-bigquery-practice-sample-fb58a943c40b.json"

def bq_create_dataset():
    bigquery_client=bigquery.Client()
    dataset_ref=bigquery_client.dataset('gcp_practice_sample')
    try:
        bigquery_client.get_dataset(dataset_ref)
    except Exception as e:
        dataset=bigquery.Dataset(dataset_ref)
        dataset_create=bigquery_client.create_dataset(dataset)
        print('Dataset {} created .'.format(dataset.dataset_id))
#bq_create_dataset()

def bq_create_table():
    bigquery_client=bigquery.Client()
    dataset_ref=bigquery_client.dataset('gcp_practice_sample_ds')
    table_ref=dataset_ref.table('Dept')
    try:
        bigquery_client.get_table(table_ref)
    except Exception as e:
        schema=[
            bigquery.SchemaField('DeptId','INTEGER',mode='REQUIRED'),
            bigquery.SchemaField('DeptName','STRING',mode='REQUIRED'),
            bigquery.SchemaField('EmpId','INTEGER',mode='REQUIRED')
        ]
        table=bigquery.Table(table_ref,schema)
        table_creation=bigquery_client.create_table(table)
        print('Table {} created .'.format(table.table_id))

#bq_create_table()

def bq_insert_rows():
    bigquery_client=bigquery.Client()
    dataset_ref=bigquery_client.dataset('gcp_practice_sample_ds')
    table_ref=dataset_ref.table('Dept')
    table=bigquery_client.get_table(table_ref)
    rows_to_insert=[
        (101,'Data_Practice',79758),
        (102,'Data_Science',79759

        )
    ]
    rows_insert=bigquery_client.insert_rows(table,rows_to_insert)
#bq_insert_rows()

def data_exists():
    bigquery_client=bigquery.Client()
    query=('Select empid ,deptid,deptname from `{}.{}.{}` where empid="{}" '.format('bigquery-practice-sample','gcp_practice_sample_ds','Dept','79758'))
    try:
        query_job=bigquery_client.query(query)
        is_exist=len(list(query_job.result())) >=1
        print('Exist id: {}'.format('79758') if is_exist else 'Not exist id ')
        return is_exist
    except Exception as e:
        print('Error')
        print(e)
    return False
data_exists()