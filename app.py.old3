import streamlit as st
import osmnx as ox
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import folium_static

# Define the example coordinates and descriptions
example_coordinates = {
    "Hagenberg, Austria": (48.36964, 14.5128),
    "Lienz (Daniel), Austria": (46.8294, 12.7687),
    "FTA-Communauté de communes du Guillestrois-Queyras, France": (44.6616, 6.6497),
    "LTA-Communauté de communes des Baronnies en Drôme Provençale, France": (44.3555, 5.1283),
    "Loeffingen-LTA (Anna), Germany": (47.8840, 8.3438),
    "Elztal-FTA (Anna), Germany": (48.1442, 8.0474),
    "Elzach-FTA (Anna), Germany": (48.1731, 8.0686),
    "Cogne (Alessio), Italy": (45.6081, 7.3527),
    "LTA (Darja), Slovenia": (46.6581, 16.1631),
    "FTA (Darja), Slovenia": (46.5530, 15.6509)    
}

def get_amenities(latitude, longitude, amenity_type='all', radius=1000):
    """
    Retrieves amenities within a given radius of the specified coordinates.
    Filters by amenity type if specified.
    """
    tags = {'amenity': True} if amenity_type == 'all' else {'amenity': amenity_type}
    amenities = ox.geometries_from_point((latitude, longitude), tags=tags, dist=radius)
    return amenities
    
def count_amenities(latitude, longitude, radius=1000):
    """
    Counts different amenities within a given radius of the specified coordinates.
    """
    point = (latitude, longitude)
    amenities = ox.geometries_from_point(point, tags={'amenity': True}, dist=radius)
    amenity_counts = amenities['amenity'].value_counts()
    return amenity_counts.to_dict()


def main():
    st.title("Smart CommUnity - TA Analyzer")

    example_choice = st.selectbox("Choose a Test Area:", list(example_coordinates.keys()))
    selected_coordinate = example_coordinates[example_choice]

    # Update latitude and longitude based on user input or selection
    lat = st.number_input("Enter the latitude of the area:", value=selected_coordinate[0])
    lon = st.number_input("Enter the longitude of the area:", value=selected_coordinate[1])
    zoom = st.slider("Zoom level:", min_value=1, max_value=10, value=5)
    dista = 200 * zoom

    # Create a Folium map centered on the selected coordinates
    m = folium.Map(location=[lat, lon], zoom_start=14)

    # Expanded list of amenities
    amenity_options = ['all', 'restaurant', 'hospital', 'school', 'bank', 'cafe', 'pharmacy', 'cinema', 'parking', 'fuel']
    amenity_type = st.selectbox("Select Amenity Type:", amenity_options)
    
    if st.button('Show Amenities'):
        try:
            amenities = get_amenities(lat, lon, amenity_type, radius=dista)
        except Exception as e:
            if "EmptyOverpassResponse" in str(e):
                st.warning(f"No {amenity_type} amenities found within the specified distance.")
                return
            else:
                raise e  # If it's a different exception, re-raise it

        # Add markers to the map for valid geometries
        for _, row in amenities.iterrows():
            if row.geometry:
                # Handle both Points and Polygons
                if row.geometry.geom_type == 'Point':
                    point_location = [row.geometry.y, row.geometry.x]
                elif row.geometry.geom_type == 'Polygon':
                    point_location = [row.geometry.centroid.y, row.geometry.centroid.x]
                else:
                    continue  # Skip if geometry is neither Point nor Polygon

                tooltip = f"{row['amenity']}: {row.get('name', 'N/A')}"
                folium.Marker(
                    location=point_location,
                    popup=tooltip,
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)
            
        # Display the map in Streamlit
        folium_static(m)
        
    # Add a button to count amenities
    if st.button('Count Amenities'):
        amenities_count = count_amenities(lat, lon, dista) 
        st.write('Amenities count within the area:')
        st.write(amenities_count)

if __name__ == "__main__":
    main()


