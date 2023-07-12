import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

# Set up the Streamlit app
st.title("SmartCommUnity - TA Analyzer")
lat = st.number_input("Enter the latitude of the area:", value=48.36)
lon = st.number_input("Enter the longitude of the area:", value=14.51)
zoom = st.slider("Zoom level:", min_value=1, max_value=18, value=10)

# Allow the user to select the data to display
show_buildings = st.checkbox("Show Buildings")
show_amenities = st.checkbox("Show Amenities")

# Retrieve the graph from OpenStreetMap
G = ox.graph_from_point((lat, lon), network_type='all', dist=1000)

# Get a list of the features (buildings and/or amenities)
features = gpd.GeoDataFrame()

if show_buildings:
    buildings = ox.geometries_from_point((lat, lon), tags={'building': True}, dist=1000)
    features = features.append(buildings)

if show_amenities:
    amenities = ox.geometries_from_point((lat, lon), tags={'amenity': True}, dist=1000)
    features = features.append(amenities)

# Set the active geometry column
features = features.set_geometry('geometry')

# Plot the graph using OSMnx
fig, ax = ox.plot_graph(G, show=False, close=False, edge_color='gray', edge_linewidth=1, edge_alpha=0.5, figsize=(10, 10))
ax.set_title('Visualization')

# Plot the features (buildings and/or amenities)
if not features.empty:
    features.plot(ax=ax, color='red', alpha=0.7)

# Display the plot in the Streamlit app
st.pyplot(fig)
