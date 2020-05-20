import plotly.express as px
import pandas as pd 
from collections import Counter

df = pd.read_csv('list_lengths.csv', header=None)

length_list = []
current_length = 0
for index, row in df.iterrows():
    command_name = row[0]
    if command_name == 'teardown':
        length_list.append(current_length)
        current_length = 0
    else:
        if command_name == 'init_state':
            continue
        else:
            current_length += 1


print(length_list)

new = pd.DataFrame({'list_length':length_list})
fig = px.histogram(new, x="list_length")
fig.update_layout(
    title_text='Hypothesis Default Example Command List Lengths',
    xaxis_title="Command List Length",
    yaxis_title="Count"
)
fig.write_html('com_length.html')
#fig.write_image("images/fig1.pdf")