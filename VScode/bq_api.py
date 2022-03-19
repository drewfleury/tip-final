#%%

from google.cloud import bigquery
import os
import pandas as pd

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/drewfleury/Documents/TIP/VScode/private_key_tipapi.json'

# variables
gcp_project = 'striped-micron-344413'
bq_dataset = 'tip_dataset_1'

# connections
client = bigquery.Client(project = gcp_project)
dataset_ref = client.dataset(bq_dataset)

def my_query(query):
    query_job = client.query(query)
    results = query_job.result()
    for row in results:
        return row

def query_to_df(query):
    return client.query(query).to_dataframe()

df_priority_raised = query_to_df('SELECT priority, COUNT(priority) AS Count FROM tip_dataset_1.raised GROUP BY priority;')
df_priority_closed = query_to_df('SELECT priority, COUNT(priority) AS Count FROM tip_dataset_1.closed GROUP BY priority;')
df_priority_backlog = query_to_df('SELECT priority, COUNT(priority) AS Count FROM tip_dataset_1.backlog GROUP BY priority;')
# %%
 