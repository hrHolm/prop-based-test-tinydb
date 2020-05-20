import plotly.express as px
import pandas as pd 
from collections import Counter

df = pd.read_csv('list_lengths.csv', header=None)

s = df[0].value_counts()
new = pd.DataFrame({'Command':s.index, 'Count':s.values})
fig = px.bar(new, x="Command", y="Count")
fig.update_layout(
    title_text='Command Generation Histogram'
)
fig.write_html('yo.html')
#fig.write_image("images/fig1.pdf")