import plotly.express as px
import pandas as pd 
from collections import Counter

df = pd.read_csv('list_lengths.csv', header=None)

pair_list = []
current_pair = []
for index, row in df.iterrows():
    command_name = row[0]
    current_pair.append(command_name)
    if current_pair[0] == 'teardown':
        current_pair = []
        continue
    if len(current_pair) == 2:
        pair_list.append(current_pair[0] + '-' + current_pair[1])
        current_pair = []


#print(pair_list)

new = pd.DataFrame({'pair_list':pair_list})
fig = px.histogram(new, x="pair_list")
fig.update_layout(
    title_text='Command Pair Distribution',
    xaxis_title="Command Pair",
    yaxis_title="Count"
)
fig.update_xaxes(categoryorder="total descending")
fig.write_html('com_pair.html')
#fig.write_image("images/fig1.pdf")
