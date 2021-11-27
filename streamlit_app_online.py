# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st

import pandas as pd
import os
from math import pi
import time

import altair as alt

from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from bokeh.plotting import figure, show




# path = "C:/Users/Karsten/OneDrive/Python Scripting/10 spitch"
# os.chdir(path)



# data import

url_df = "https://github.com/flxmac/kantersieg/blob/9b75430a532486740f87e1736e1525551b29763c/spitch.xlsx"
df = pd.read_excel(url_df, sheet_name = "S - 20,21 - Daten")

url_ref = "https://github.com/flxmac/kantersieg/blob/9b75430a532486740f87e1736e1525551b29763c/ref.xlsx"
ref = pd.read_excel(url_ref)


# path = r"C:\Users\Karsten\OneDrive\Python Scripting\23 streamlit dashboard\Dateien"
# os.chdir(path)


# # SETUP ------------------------------------------------------------------------
# st.set_page_config(page_title='Katersieg Cockpit',
#                     page_icon="https://cdn.pixabay.com/photo/2018/04/25/22/10/silhouette-3350710_1280.png",
#                     layout="wide")


col1, col2 = st.columns(2)
with col1:
    st.title("Kantersieg")
    
with col2:
    st.image("https://cdn.pixabay.com/photo/2018/04/25/22/10/silhouette-3350710_1280.png", width = 50)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Spieltag", df["Spieltag"].max())
    
with col2:
    points = df["Punkte"].sum()
    st.metric("Vergebene Punkte", f"{points:,}".replace(",", "."))
    
with col3:
    st.metric("Teilnehmende Spieler", int(df["Spieler"].nunique()))


# print(type(df["Punkte"].sum()))
### first chart


# chart.save("test.html")

# st.altair_chart(line_chart, use_container_width=True)



# scatter_chart.save("test.html")

# with st.expander("Ballon Chart"):


### Spieler

st.subheader("Saisonübersicht")


with st.expander("Whisker Box-Plot"):
    
    box_plot = alt.Chart(df).mark_boxplot(extent='min-max').encode(
        x= alt.X('Spieler:O'),
        y='Punkte:Q'       
        
    ).configure_axisX(
        labelAngle = -45
        )
    
    # box_plot.save("test.html")
    
    st.altair_chart(box_plot, use_container_width=True)
    
    st.text('Wie verteilt sich die Punktausbeute der jeweiligen Spieler')

with st.expander("Wer war wann auf welchem Platz?"):

    # st.header("Box Plot")
    scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
        x='Spieltag',
        y='Punkte',
        color='Spieler',
        tooltip=['Punkte', 'Spieltag'],
        size = "Punkte"
    ).interactive()
    
    st.altair_chart(scatter_chart, use_container_width=True)  
    
    
    st.text("Einfache Übersicht, wer an welche Spieltag wie viele Punkte geholt hat.")
    
      
with st.expander("Wer holt wie seine Punkte?"):
    ### fourth chart
    
    norm_bar = alt.Chart(df).mark_bar().encode(
        x=alt.X("Punkte"),
        y='Spieler',
        color = alt.Color('Punkte', scale=alt.Scale(scheme='redyellowgreen'))
    )
    
    st.altair_chart(norm_bar, use_container_width=True)
    
    st.text("Und einmal nach Spielern geordnet.")
    
 
with st.expander("Und wer holt Positionen?"):
    bar2 = alt.Chart(df).mark_bar().encode(
        x= alt.X("Spieltag", axis=alt.Axis(labels=False)),
        y = "Spieler",
        color = alt.Color("Platzierung Spieltag",title = "Platzierung", scale = alt.Scale(scheme = "blueorange"))
        )
    
    st.altair_chart(bar2, use_container_width = True)
    
    st.text("Im Fußball ist die Anzahl der Punkte wichtiger, als die Anzahl der Tore...")
    st.text("...bei Spitch ist die Platzierung wichtiger als die Anzahl der Punnkte!")

##################

st.subheader("Spieltagsübersicht")

with st.expander("Spieltagsübersicht"):
    
    spieltag = st.select_slider("Wähle deinen Spieltag", options = list(df["Spieltag"].unique()))
    
    
    

             
    def get_spieltag_winner(spieltag):
        spieltag_df = df[df["Spieltag"] == spieltag] 
        df_wotd = spieltag_df[spieltag_df["Punkte"] == spieltag_df["Punkte"].max()]
        wotd_spieler = df_wotd["Spieler"].iloc[0]
        # wotd_platzierung_gesamt = df_wotd["Platzierung Gesamt"].iloc[0]
        wotd_pic_link = df_wotd.merge(ref[["Spieler","pic"]], on = "Spieler").iloc[0]["pic"]
        wotd_punkte = df_wotd["Punkte"].iloc[0]
        return wotd_spieler, wotd_punkte
        
    wotd_spieler, wotd_punkte = get_spieltag_winner(spieltag)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://cdn.pixabay.com/photo/2018/01/05/17/06/silhouette-3063375_1280.png")
        
    with col2:
        st.metric("Gewinner des Spieltags", value = wotd_spieler)
        st.metric("Punkte", value = f"{wotd_punkte:,}".replace(",", "."))
        
        


    
    def get_spieltag_loser(spieltag):
        spieltag_df = df[df["Spieltag"] == spieltag] 
        df_lotd = spieltag_df[spieltag_df["Punkte"] == spieltag_df["Punkte"].min()]
        lotd_spieler = df_lotd["Spieler"].iloc[0]
        # wotd_platzierung_gesamt = df_wotd["Platzierung Gesamt"].iloc[0]
        lotd_pic_link = df_lotd.merge(ref[["Spieler","pic"]], on = "Spieler").iloc[0]["pic"]
        lotd_punkte = df_lotd["Punkte"].iloc[0]
        return lotd_spieler, lotd_punkte
        
    lotd_spieler, lotd_punkte = get_spieltag_loser(spieltag)
    
    col1, col2 = st.columns(2)
        
    with col1:
        st.metric("Verlierer des Spieltags", value = lotd_spieler)
        st.metric("Punkte", value = f"{lotd_punkte:,}".replace(",", "."))
    with col2:
        st.image("https://cdn.pixabay.com/photo/2018/04/24/17/40/silhouette-3347559_1280.png")



############

st.subheader("Wer hat im Direktvergleich die Nase vorn?")
with st.expander("Auf in den Zweikampf..."):
    
    st.image("https://cdn.pixabay.com/photo/2021/03/13/15/20/boxing-6091981_1280.png")
    
    col1, col2 = st.columns(2)
    
    with col1: 
        
        p1 = st.selectbox(label = "Wähle einen Spieler", options = list(df["Spieler"].unique()))
        df_p1 = df[df["Spieler"] == p1]
        p1_min, p1_mean, p1_median, p1_max = df_p1["Punkte"].min(), df_p1["Punkte"].mean(), df_p1["Punkte"].median(), df_p1["Punkte"].max()
        p1_values = [p1_min, p1_mean, p1_median, p1_max]
        p1_list = [*p1_values, p1_values[0]]

        
        
        
    with col2:
        p2 = st.selectbox(label = "Wähle einen Gegner", options = list(df["Spieler"].unique()))
        
        df_p2 = df[df["Spieler"] == p2]
        p2_min, p2_mean, p1_median, p2_max = df_p2["Punkte"].min(), df_p2["Punkte"].mean(), df_p1["Punkte"].median(), df_p2["Punkte"].max()
        p2_values = [p2_min, p2_mean, p1_median, p2_max]
        p2_list = [*p2_values, p2_values[0]]

        
        
    categories = ["Minimale Punkte", "Durchschnittliche Punkte pro Spieltag","Median", "Maximale Punkte"]
    categories = [*categories, categories[0]]
    spidernet = go.Figure(
        data=[
            go.Scatterpolar(r=p1_list, theta=categories,  name=p1),
            go.Scatterpolar(r=p2_list, theta=categories,  name=p2)
        ],
        layout=go.Layout(
            title=go.layout.Title(text='1 gegen 1'),
            polar={'radialaxis': {'visible': True}},
            showlegend=True
        )
    )
    
    st.plotly_chart(spidernet, use_container_width = True)
       


############

# loser = df[df["Platzierung Spieltag"] == 8]
# loser["counter"] = 1


st.subheader("La tapa")
with st.expander("Der Deckel"):
    loser = df[df["Platzierung Spieltag"] == 8]
    loser["counter"] = 5
    loser = loser.pivot_table(index = "Spieler", values = "counter", aggfunc = "sum" )

    
    
    loser['angle'] = loser['counter']/loser['counter'].sum() * 2*pi
    
    loser['color'] = Category20c[len(loser["counter"])]
    
    p = figure(title="Die Abrechnung", toolbar_location=None,
               tools="hover", tooltips="@Spieler: @counter", x_range=(-0.5, 1.0))
    
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", legend_field='Spieler', fill_color = "color", source=loser)
    
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    
    
    st.bokeh_chart(p, use_container_width=True)
    
    st.text("Alle Bußgelder in €...")



st.subheader("Pferderennen")

### calculate cumsum
df["cumsum"] = df["Punkte"].cumsum()

line_chart = alt.Chart(df).mark_line().encode(
    # x='Spieltag',
    # y='Punkte',
    # color = "Spieler"
    )

# Plot a Chart
def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
    x=alt.X('Spieltag', axis=alt.Axis(title='Spieltag')),
    y=alt.Y('cumsum',axis=alt.Axis(title='Punkte')),
    color = "Spieler"
    )
    return lines

N = df.shape[0] # number of elements in the dataframe
burst = 1       # number of elements (months) to add to the plot
size = burst    # size of the current dataset

# Plot Animation
line_plot = st.altair_chart(line_chart, use_container_width = True)
start_btn = st.button('Start')

if start_btn:
    for i in range(1,N):
        step_df = df.iloc[0:size]       
        lines = plot_animation(step_df)
        line_plot = line_plot.altair_chart(lines, use_container_width= True)
        size = i + burst
        if size >= N:
            size = N - 1  
        time.sleep(0.001)      
        
