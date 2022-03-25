#%%

from google.cloud import bigquery
import os
import pandas as pd

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key_tipapi.json'

# variables
gcp_project = 'striped-micron-344413'
bq_dataset = 'tip_dataset_1'

# connections
client = bigquery.Client(project = gcp_project)
dataset_ref = client.dataset(bq_dataset)

"""def my_query(query):
    query_job = client.query(query)
    results = query_job.result()
    for row in results:
        return row"""

def query_to_df(query):
    return client.query(query).to_dataframe()

df_priority_raised = query_to_df('SELECT priority, COUNT(priority) AS Count FROM tip_dataset_1.raised GROUP BY priority;')
df_priority_closed = query_to_df('SELECT priority, COUNT(priority) AS Count FROM tip_dataset_1.closed GROUP BY priority;')
df_priority_backlog = query_to_df('SELECT priority, COUNT(priority) AS Count FROM tip_dataset_1.backlog GROUP BY priority;')

Average_res_time_raised = query_to_df('SELECT Priority, AVG(TIMESTAMP_DIFF(Resolution_Date_Time, Create_Date_Time, MINUTE)/60) AS AVE_Resolution_time_hours FROM tip_dataset_1.raised GROUP BY Priority')
Average_res_time_closed = query_to_df('SELECT Priority, AVG(TIMESTAMP_DIFF(Resolution_Date_Time, Creation_Date_Time, MINUTE)/60) AS AVE_Resolution_time_hours FROM tip_dataset_1.closed GROUP BY Priority')
Average_res_time_backlog = query_to_df('SELECT Priority, AVG(TIMESTAMP_DIFF(Resolution_Date_Time, Creation_Date_Time, MINUTE)/60) AS AVE_Resolution_time_hours FROM tip_dataset_1.backlog GROUP BY Priority')

issue_cause_raised = query_to_df('SELECT Inc__Type, COUNT(Inc__Type) AS Incident_Count FROM tip_dataset_1.raised GROUP BY Inc__Type ORDER BY Incident_Count DESC')
issue_cause_closed = query_to_df('SELECT Inc__Type, COUNT(Inc__Type) AS Incident_Count FROM tip_dataset_1.closed GROUP BY Inc__Type ORDER BY Incident_Count DESC')
issue_cause_backlog = query_to_df('SELECT Inc__Type, COUNT(Inc__Type) AS Incident_Count FROM tip_dataset_1.backlog GROUP BY Inc__Type ORDER BY Incident_Count DESC')

weekly_incidents_riaised = query_to_df('SELECT EXTRACT(WEEK FROM Create_Date_Time) AS Week, EXTRACT(YEAR FROM Create_Date_Time) AS Year, COUNT(Create_Date_Time) AS Incident_Count FROM tip_dataset_1.raised \
GROUP BY Week, Year')
weekly_incidents_closed = query_to_df('SELECT EXTRACT(WEEK FROM Creation_Date_Time) AS Week, EXTRACT(YEAR FROM Creation_Date_Time) AS Year, COUNT(Creation_Date_Time) AS Incident_Count FROM tip_dataset_1.closed \
WHERE EXTRACT(YEAR FROM Creation_Date_Time) = 2021 GROUP BY Week, Year ORDER BY Week')
weekly_incidents_backlog = query_to_df('SELECT EXTRACT(WEEK FROM Creation_Date_Time) AS Week, EXTRACT(YEAR FROM Creation_Date_Time) AS Year, COUNT(Creation_Date_Time) AS Incident_Count FROM tip_dataset_1.backlog \
WHERE EXTRACT(YEAR FROM Creation_Date_Time) = 2021 GROUP BY Week, Year ORDER BY Week')

weekly_incidents_closed
 
# %%
