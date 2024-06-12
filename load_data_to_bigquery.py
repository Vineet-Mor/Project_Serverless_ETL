!pip install google-cloud-bigquery
from google.cloud import bigquery
from datetime import datetime
client = bigquery.Client(project="quixotic-treat-419302")

#dataset_id = "{}.your_dataset".format(client.project)
current_time=datetime.now().date()
date=current_time.strftime("%y-%m-%d").split("-")[-1]
month=current_time.strftime("%y-%m-%d").split("-")[-2]
date=29
month=4
dataset_id=f"quixotic-treat-419302.flights_{month}_2024"
print(dataset_id)

try:
    client.get_dataset(dataset_id)  # Make an API request.
    print("Dataset {} already exists".format(dataset_id))
except:
    dataset = bigquery.Dataset(dataset_id)
    #dataset.location = "US"
    print(dataset)
    dataset = client.create_dataset(dataset, timeout=30) 
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))


table_id = dataset_id+f".flights_2024_{month}_{date}"
print(table_id)
schema = [
    bigquery.SchemaField("flight_date", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("airline_code", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("flight_num", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("source_airport", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("destination_airport", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("departure_time", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("departure_delay", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("arrival_time", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("arrival_delay", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("airtime", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("distance", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    ]
try:
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
except:
    print("table already exist")


project_id = "quixotic-treat-419302"
job_config = bigquery.LoadJobConfig(
    schema=schema,
    #skip_leading_rows=0,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
)
uri ="gs://new_project_data_vm/flight_data/2023-01-27.json"
load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)  # Make an API request.

load_job.result()
column_name="item_id"
table=f"flights_{month}_2024.flights_2024_{month}_{date}"
item_id="id"
Query=f"SELECT * FROM (SELECT *, row_number() over (partition by {item_id}) as rn FROM {table}) x WHERE x.rn>1"
query_job=client.query(Query)
rows0=query_job.result()
Query1=(f"DELETE FROM {table} WHERE {item_id} in (SELECT {item_id} FROM {table} GROUP BY {item_id} HAVING COUNT({item_id})>1)")
query1_job=client.query(Query1)
rows1=query1_job.result()
for row in rows0:
    print(row)
    cols="flight_date,airline_code,flight_num,source_airport,destination_airport,departure_time,departure_delay,arrival_time,arrival_delay,airtime, distance,id"
    val=f'{row[0]},{row[0]},{row[0]},{row[0]},{row[0]},{row[0]},{row[0]},{row[0]},{row[0]},{row[0]},{row[0]},{row[0]}'
    
    Query3=(f"INSERT INTO {table}({cols}) VALUES(val)")
    query3_job=client.query(Query3)
    results=query3_job.result()
destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))
