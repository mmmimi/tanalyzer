# Import the required libraries
import osmnx as ox
import geopandas as gpd
import pandas as pd
import streamlit as st

# Define the example coordinates and descriptions
example_coordinates = {
    "Hagenberg, Austria": (48.36964, 14.5128),
    "Lienz (Daniel), Austria": (46.8294, 12.7687),
    "FTA-Communauté de communes du Guillestrois-Queyras , France": (44.6616, 6.6497),
    "LTA-Communauté de communes des Baronnies en Drôme Provençale, France": (44.3555, 5.1283),
    "Loeffingen-LTA (Anna), Germany": (47.8840, 8.3438),
    "Elztal-FTA (Anna), Germany": (48.1442, 8.0474),
    "Elzach-FTA (Anna), Germany": (48.1731, 8.0686),
    "Cogne (Alessio), Italy": (45.6081, 7.3527),
    "LTA (Darja), Slovenia": (46.6581, 16.1631),
    "FTA (Darja), Slovenia": (46.5530, 15.6509)    
}

def count_amenities(latitude, longitude, radius=1000):
    """
    Counts different amenities within a given radius of the specified coordinates.
    """
    point = (latitude, longitude)
    amenities = ox.geometries_from_point(point, tags={'amenity': True}, dist=radius)
    amenity_counts = amenities['amenity'].value_counts()
    return amenity_counts.to_dict()

def main():
    # Set up the Streamlit app
    st.title("Smart CommUnity - TA Analyzer")

    # Add a selection menu for the user to choose an example
    example_choice = st.selectbox("Choose a Test Area:", list(example_coordinates.keys()))

    # Retrieve the selected example coordinates
    selected_coordinate = example_coordinates[example_choice]
    lat = st.number_input("Enter the latitude of the area:", value=selected_coordinate[0])
    lon = st.number_input("Enter the longitude of the area:", value=selected_coordinate[1])
    zoom = st.slider("Zoom level:", min_value=1, max_value=10, value=5)
    
    dista = 200 * zoom

    # Allow the user to select the data to display
    st.write("Select data to display:")
    col1, col2 = st.columns(2)

    with col1:
        show_buildings = st.checkbox("Show Buildings")

        show_amenities = st.checkbox("Show Amenities")

    with col2:
        show_emergencies = st.checkbox("Show Emergencies")

        show_commercial_land = st.checkbox("Show Commercial Land")
        
    # Define colors for each feature type
    feature_colors = {
        "building": "red",
        "amenity": "green",
        "emergency": "blue",
        "commercial_land": "yellow"
    }


    # Retrieve the graph from OpenStreetMap
    G = ox.graph_from_point((lat, lon), network_type='all', dist=dista)

    # Get a list of the features (buildings and/or amenities)
    features = []

    if show_buildings:
        try:
            buildings = ox.geometries_from_point((lat, lon), tags={'building': True}, dist=1000)
            buildings["feature_type"] = "building"  # Add a new column to specify the feature type
            features.append(buildings)
        except:
            st.warning("No buildings found within the specified distance.")

    if show_amenities:
        try:
            amenities = ox.geometries_from_point((lat, lon), tags={'amenity': True}, dist=1000)
            amenities["feature_type"] = "amenity"  # Add a new column to specify the feature type
            features.append(amenities)
        except:
            st.warning("No amenities found within the specified distance.")
            
    if show_emergencies:
        try:
            emergencies = ox.geometries_from_point((lat, lon), tags={'emergency': True}, dist=1000)
            emergencies["feature_type"] = "emergency"  # Add a new column to specify the feature type
            features.append(emergencies)
        except:
            st.warning("No emergencies found within the specified distance.")
    
    if show_commercial_land:
        try:
            commercial_land = ox.geometries_from_point((lat, lon), tags={'landuse': 'commercial'}, dist=1000)
            commercial_land["feature_type"] = "commercial_land"  # Add a new column to specify the feature type
            features.append(commercial_land)
        except:
            st.warning("No commercial land found within the specified distance.")



    # Concatenate the features GeoDataFrames
    if len(features) > 0:
        features = gpd.GeoDataFrame(pd.concat(features, ignore_index=True), crs="EPSG:4326")

    # Plot the graph using OSMnx
    fig, ax = ox.plot_graph(G, show=False, close=False, edge_color='gray', edge_linewidth=1, edge_alpha=0.5, figsize=(10, 10))
    ax.set_title('Visualization')

    # Plot the features (buildings and/or amenities) with different colors
    for feature_type, color in feature_colors.items():
        if len(features) > 0:
            filtered_features = features[features["feature_type"] == feature_type]
            if not filtered_features.empty:
                filtered_features.plot(ax=ax, color=color, alpha=0.7)

    # Display the plot in the Streamlit app
    st.pyplot(fig)


    # Add a button to count amenities
    if st.button('Count Amenities'):
        amenities_count = count_amenities(lat, lon, dista) 
        st.write('Amenities count within the area:')
        st.write(amenities_count)

if __name__ == "__main__":
    main()
