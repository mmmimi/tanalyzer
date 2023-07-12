import osmnx as ox
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set up the Streamlit app
st.title("OpenStreetMap Data Visualization")
lat = st.number_input("Enter the latitude of the area:", value=48.34)
lon = st.number_input("Enter the longitude of the area:", value=14.49)
zoom = st.slider("Zoom level:", min_value=1, max_value=18, value=10)

# Allow the user to select the data to display
show_buildings = st.checkbox("Show Buildings")
show_amenities = st.checkbox("Show Amenities")

# Retrieve the graph from OpenStreetMap
G = ox.graph_from_point((lat, lon), network_type='all', dist=1000)

# Get a list of the features (buildings and/or amenities)
features = []

if show_buildings:
    buildings = ox.geometries_from_point((lat, lon), tags={'building': True}, dist=1000)
    features.append(buildings)


if show_amenities:
    try:
        amenities = ox.geometries_from_point((lat, lon), tags={'amenity': True}, dist=1000)
        features.append(amenities)
    except:
        st.warning("No amenities found within the specified distance.")

# Concatenate the features GeoDataFrames
if len(features) > 0:
    features = gpd.GeoDataFrame(pd.concat(features, ignore_index=True), crs="EPSG:4326")

# Plot the graph using OSMnx
fig, ax = ox.plot_graph(G, show=False, close=False, edge_color='gray', edge_linewidth=1, edge_alpha=0.5, figsize=(10, 10))
ax.set_title('OpenStreetMap Data Visualization')

# Plot the features (buildings and/or amenities)
if len(features) > 0:
    features.plot(ax=ax, color='red', alpha=0.7)

# Display the plot in the Streamlit app
st.pyplot(fig)