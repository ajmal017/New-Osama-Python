import numpy as np
import pandas as pd

df = pd.read_csv('D:\Python\Project\example')
print(df)
df.to_csv('D:\Python\Project\example',index=False)
print(df)
exell=pd.read_excel('D:\Python\Project\Excel_Sample.xlsx',sheet_name='Sheet1')
print(exell)
df = pd.read_html('http://www.fdic.gov/bank/individual/failed/banklist.html')
print(df)