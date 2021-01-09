from classes.ensemble import Ensemble
from classes.world import World
from classes.constants import VEG_IM, ELV_IM, AFROEURASIA
import streamlit as st
import PIL
from PIL import Image
'''
  Local URL: http://localhost:8501
  Network URL: http://192.168.0.18:8501
'''
#https://discuss.streamlit.io/t/how-to-pause-a-simulation-app-and-resume-from-where-you-stopped/5693/4 pause button
def main():
    #world = World("vegetation_map_with_key.png", "elevation_map.png")



    st.title("CivSim")
    st.subheader("Simulation utilizing cellular automata")

    #slider for the number of steps
    st.sidebar.text("In this simulation, the cells on the \nedges of civilizations have a chance to \ncolonize neighbors or go extinct based \nupon the vegatation, elevation, and a \nrandomized percent colonization. ")
    teams = st.sidebar.slider("Number of players", min_value = 5, max_value = 15, step = 1, value = 10)
    steps = st.sidebar.slider("Number of decade-long time steps", min_value = 100, max_value = 2200, step= 100, value = 800)
    image = Image.open("afroeurasia.png")
    st_image = st.image(image, use_column_width = True)
    age_text = st.sidebar.text("Current Time: 20000 BC")
    progress_bar = st.sidebar.progress(0)
    
    world = World(VEG_IM, ELV_IM, teams)
    ensemble = Ensemble(world, AFROEURASIA)
    age = -20000
    if st.sidebar.button("Run Simulation"):
        running = True
        while running:
            counter = 0
            while counter < steps:
                    age = ensemble.run(age, counter, st_image, age_text, progress_bar, steps)
                    counter += 1
            running = False

main()