import json 
import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch
st.title("Euro 2024 mapa de chutes")
st.subheader("Filtrar por seleção ou jogador para ver os chutes!")
df = pd.read_csv("euros_2024_shot_map.csv")
print(df.head())
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)
team = st.selectbox("Selecione a seleção", df['team'].unique())
player = st.selectbox("Selecione o jogador", df[df['team'] == team]['player'].sort_values().unique(), index = None)
def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]

    return df
filtered_df = filter_data(df, team, player)
pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(10, 10))
def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x = float(x['location'][0]),
            y = float(x['location'][1]),
            ax = ax,
            s = 1000*x['shot_statsbomb_xg'],
            color = 'green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolor = 'black',
            alpha = 1 if x['shot_outcome'] == 'Goal' else 0.5,
            zorder = 1 if x['shot_outcome'] == 'Goal' else 0.5
        )
plot_shots(filtered_df, ax, pitch)
st.pyplot(fig)
