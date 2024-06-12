import glob
import os
from google.cloud import storage
gsclient=storage.Client(project="quixotic-treat-419302")
src_dir="D:/Data Engineering Training/Flight data"
tgt_dir="flight_data"
def get_file_names(src_base_dir):
    items=glob.glob(f'{src_base_dir}/**',recursive=True)
    print(items)
    return list(filter(lambda item:os.path.isfile(item),items ))
def get_file_name(path):
    return path.split('\\')[1].split('.')[0]+".json"
bucket=gsclient.get_bucket('new_project_data_vm')
files=get_file_names(src_dir)
print(files)
for file in files:
    print(f"uploading file {file}")
    blob_suffix=get_file_name(file)
    blob_name=f'{tgt_dir}/{blob_suffix}'
    blob=bucket.blob(blob_name)
    blob.upload_from_filename(file)
