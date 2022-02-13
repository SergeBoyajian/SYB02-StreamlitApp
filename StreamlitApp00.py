import pandas as pd
import numpy as np
import streamlit as st
#py.offline.init_notebook_mode(connected = True)  # this sets plotly  to offline mode
import chart_studio.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

#Creating the sidebar
rad= st.sidebar.radio("Navigation", ["Home", "UFO Dataset", "Cameras Dataset"])


if rad == "Home":
    st.image("https://i0.wp.com/gbsn.org/wp-content/uploads/2020/07/AUB-logo.png?ssl=1", width=300)
    #st.image(image="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png")
    st.title("Welcome to my first Streamlit App")
    st.markdown("My name is Serge Boyajian and you are currently viewing my first Streamlit app. Building it was fun, interesting and extremely educational for me. However, I faced some issues along the way like publishing the app, creating a sidebar and trying widgets. In this app, we will explore some Plotly visualizations on 2 different datasets: UFO sightings in the last century and camera information. I am so happy and satisfied with the results displayed although they might seem primitive to experts and I am looking forward to build richer and more interactive Streamlit apps in the future.")

if rad == "UFO Dataset":
    st.title("Dataset 1: UFO sightings in the last decade")
    #Loading the first dataset: UFO
    @st.cache
    def load_data(nrows):
        ufo=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vS5gb32QP3SNIvyPK8pzlCYoMQsTGALfaQnIjSMmj2eRLLP9EAGjGarLxyByIAGnKT0dsiRt3k9WfXd/pub?gid=36354335&single=true&output=csv", nrows=nrows)
        return ufo

    ufo_load_state= st.text("Loading data...")
    ufo= load_data(70000)
    ufo_load_state.text("Data was loaded successfully")

    st.subheader("Raw Data: ")
    if st.button("Click to See Raw Data", key=1):
        st.write(ufo)

    st.header("Objective:")
    st.markdown("This dataset includes information about UFO sightings in different locations accross the world. The purpose of this section's visuals is to identify the average duration of sightings in different countries, build a trend on UFO sightings, identify which shapes are most spotted in the sky and finally visualize the sightings using a heatmap.")

    #Fact Check section
    st.subheader("Fact Check")
    st.markdown("Before moving on, I'd like you to take a small test for you to test your knowledge about UFO sightings around the world.  \n"
    "The question is the following: In your opinion, which country had the highest UFO sightings during the last century ?")
    rad2= st.radio("Pick a country", ["","Canada", "United Kingdom","United States", "Australia"])
    if rad2 == "":
        st.text("")
    if rad2 == "Canada":
        st.text("Wrong answer! Try another time...")
    if rad2 == "United Kingdom":
        st.text("Not what we expect! The UK is too peaceful for Aliens anyways...")
    if rad2 == "Australia":
        st.write("Australia is a pretty crazy country but not in this case :smile: ")
    if rad2 == "United States":
        st.text("Correct!")
        st.balloons()

    #Visualizing UFO sightings per country
    st.header("1-Histogram-UFO Sightings per Country")
    fig=px.histogram(ufo, x="country", labels={"country": "Country"})
    st.write(fig)
    st.markdown("As seen above, The US had the highest UFO sightings at around 66,000. Australia & UK fall last with 10 observations only!")

    #Visualizing the average duration of all sightings per country
    st.header("2-Histogram-Average Duration of Each UFO Sighting per Country")
    a=ufo.groupby(ufo['country']).mean('duration (seconds)')
    aa=a.reset_index()
    data1 = [go.Bar(x=aa.country,
                    y=aa['duration (seconds)'])]
    layout1 = go.Layout(title="Average Duration of UFO Sightings per Country",
                xaxis=dict(title='Country'),
                yaxis=dict(title='Duration (in seconds)'))
    fig1 = go.Figure(data=data1, layout=layout1)
    st.write(fig1)
    st.markdown("Interesting findings! Although the UK had the lowest number of UFO sightings, it had the highest average duration in terms of seconds. The UK had the highest average duration of UFO sightings of 500 seconds and Canada had the lowest average of around 200 seconds.")
    #Displaying a scatterplot of each year's total duration of UFO sightings
    st.header("3-Scatterplot- Total UFO sightings duration per year")
    b=ufo.groupby(['year'])['duration (seconds)'].sum().reset_index()
    fig2= px.scatter(b, x='year', y='duration (seconds)')
    st.write(fig2)
    st.markdown("A clear trend is displayed in the figure: The duration of UFO sightings are increasing as time goes by. In fact, back in 2013, planet Earth had its skies occupied by UFOs around 5% of the whole year (as a duration metric).")

    #Countplot of UFO Shapes Sighted
    st.header("4- Countplot- Most Spotted UFO Shapes")
    data3 = [
            go.Bar(
            y=ufo['shape'].value_counts(ascending=True).keys(),
            x=ufo['shape'].value_counts(ascending=True),
            orientation='h',
                )]
    layout3 = go.Layout(
        title='Most Spotted UFO Shapes',
        xaxis=dict(title='Count'),
        yaxis=dict(title='',ticklen=5, gridwidth=2),
        showlegend=False,
                )
    fig3 = go.Figure(data=data3, layout=layout3)
    st.write(fig3)
    st.markdown("The top three most spotted UFO shapes are: Light, Triangle and Circle")

    #Displaying a heatmap of UFO sightings across the years
    st.header("5-Heatmap-UFO Sightings Across the Years")
    ufo=ufo.sort_values('year', ascending=True)
    fig4 = px.density_mapbox(ufo, lat = "latitude", lon ="longitude", z = "duration (seconds)", radius = 10,
    center = dict(lat = 8, lon =8), zoom = 1, hover_name = 'city',
    mapbox_style = 'carto-positron', title = 'UFO Sightings Heatmap Map', animation_frame="year")
    st.write(fig4)
    st.markdown("The heatmap found above visualizes the UFO sightings while color coding the duration in seconds. We can spot that the majority of sightings were in Canada and USA.")


if rad == "Cameras Dataset":
    st.title("Dataset 2: Exploring data about different camera models")
    #Using A NEW DATASET: CAMERA
    #Loading the dataset to Streamlit
    @st.cache
    def load_data2(nrows):
        camera=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTZ6ZMU8ly2SYmqaWnDCLjY92jMAOinSfiZbKnykMLaYWFR295c0Mkps5MEZSD9Gw3a_FdFHsmRtHG7/pub?gid=941118692&single=true&output=csv")
        camera.replace(0, np.nan, inplace=True)
        camera.dropna(inplace=True)
        camera.sort_values("Release date", inplace=True)
        return camera

    camera_load_state= st.text("Loading data...")
    camera= load_data2(1200)
    camera_load_state.text("Data was loaded successfully")

    st.subheader("Raw Data: ")
    if st.button("Click to See Raw Data", key=2):
        st.write(camera)

    st.header("Objective:")
    st.markdown("This dataset includes information about various camera models as seen in the raw data section. The ultimate goal of this visualization section is to determine which characteristics in a camera affects effective pixels the most. That is becauseEffective pixels are the pixels that capture the image data. They are effective and by definition, effective means successful in producing the desired effect or intended result. These are the pixels that are doing the work of capturing a picture. ")
    #Animated Scatter Plot
    st.header("1- Relationship Effective pixels-Maximum resolution, Size by Price")
    st.write(px.scatter(camera, x='Max resolution', y='Effective pixels', size='Price'))
    st.markdown("As seen above, the higher the maximum resolution, the higher the effective pixels.")

    st.header("2- Relationship Effective pixels-Minimum resolution, Size by Price")
    st.write(px.scatter(camera, x="Low resolution", y="Effective pixels", size="Price"))
    st.markdown("As seen above, the higher the minimum resolution, the higher the effective pixels.")

    st.markdown("However, there is something going on!! Effective pixels vary with both maximum and minimum resolutions? Are they dependent on one feature more than the other? How are cameras priced? To find out, the three metrics will be combined into a 3D graph in section 3 to finally determine what achieves higher effective pixels.")
    #3D plot Price-Low Resolution- Max Resolution
    st.header("3- 3D Plot- Effective Pixels-Max Resolution- Low Resolution")
    fig = px.scatter_3d(camera, y = 'Max resolution', x = 'Low resolution', z = 'Effective pixels', hover_name='Model',color = 'Price',  color_discrete_sequence=px.colors.qualitative.Alphabet)
    td=fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    st.write(td)
    st.markdown("The 3D plot above unlocks an interesting insight about how effective pixels are achieved based on both maximum and minimum resolution. As noticed, a camera cannot achieve higher effective pixels without improving both the max and min resolutions together! In addition, it is interesting to note that some cameras have higher effective pixels with a lower price. Those findings encourage camera users to dig deeper into what drives their cameras' prices.")
