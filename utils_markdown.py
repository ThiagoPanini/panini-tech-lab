import os 
import json
import pandas as pd

DATA_PATH = 'data'
FOLDER = 'activity-data'
CAMINHO = os.path.join(DATA_PATH, FOLDER)
SAMPLE = os.path.join(CAMINHO, os.listdir(CAMINHO)[0])
print(SAMPLE)

with open(SAMPLE, 'rb') as f:
    file = f.readline().decode()

print(file)

json_file = json.loads(file)
df = pd.DataFrame.from_dict(json_file, orient='index').T
cols = list(df.columns)
values = df.values[0]

mk_cols = ['| ' + c  + '|' for c in cols]

