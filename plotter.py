import plotly.express as px
import pandas as pd 
from collections import Counter

df = pd.read_csv('list_lengths.csv', header=None)

s = df[0].value_counts()
new = pd.DataFrame({'Length':s.index, 'Count':s.values})
fig = px.bar(new, x="Length", y="Count")
fig.write_html('yo.html')