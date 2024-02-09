import streamlit as st
import osmnx as ox
import folium
from streamlit_folium import folium_static

# Constants
RADIUS = 1000
DEFAULT_COORDINATES = (48.36964, 14.5128)

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

def get_amenities(latitude, longitude, amenity_type='all', radius=RADIUS):
    tags = {'amenity': True} if amenity_type == 'all' else {'amenity': amenity_type}
    amenities = ox.features_from_point((latitude, longitude), tags=tags, dist=radius)
    return amenities

def count_amenities(latitude, longitude, radius=RADIUS):
    point = (latitude, longitude)
    amenities = ox.features_from_point(point, tags={'amenity': True}, dist=radius)
    amenity_counts = amenities['amenity'].value_counts()
    return amenity_counts.to_dict()

def get_smart_entities(latitude, longitude, ent, radius=RADIUS):
    parts = ent.split('=')
    tags = {parts[0]: parts[1]}
    entities = ox.features_from_point((latitude, longitude), tags=tags, dist=radius)
    return entities

def add_markers_to_map(m, entities, entity_type):
    for _, row in entities.iterrows():
        if row.geometry:
            if row.geometry.geom_type == 'Point':
                point_location = [row.geometry.y, row.geometry.x]
            elif row.geometry.geom_type == 'Polygon':
                point_location = [row.geometry.centroid.y, row.geometry.centroid.x]
            else:
                continue

            tooltip = f"{entity_type}: {row.get('name', 'N/A')}"
            folium.CircleMarker(
                location=point_location,
                radius=10,  # This controls the size of the marker. Change it as needed.
                popup=tooltip,
                color="blue",
                fill=True,
                fill_color="blue"
            ).add_to(m)

def main():
    st.title("Smart CommUnity - TA Analyzer")
    example_choice = st.selectbox("Choose a Test Area:", list(example_coordinates.keys()), key='example_choice')
    selected_coordinate = example_coordinates[example_choice]
    lat = st.number_input("Enter the latitude of the area:", value=selected_coordinate[0])
    lon = st.number_input("Enter the longitude of the area:", value=selected_coordinate[1])
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Default", "SmartEconomy", "SmartGovernance", "SmartMobility", "SmartEnvironment", "SmartPeople", "SmartLiving"])

    # Define m here
    m = folium.Map(location=[lat, lon], zoom_start=14)

    with tab1:
        # Expanded list of amenities
        amenity_options = ['all', 'restaurant', 'hospital', 'school', 'bank', 'cafe', 'pharmacy', 'cinema', 'parking', 'fuel']
        amenity_type = st.selectbox("Select Amenity Type:", amenity_options,  key='amenity_type' )
        
        if st.button('Show Amenities', key='amenity' ):
            try:
                amenities = get_amenities(lat, lon, amenity_type, RADIUS)
            except Exception as e:
                if "EmptyOverpassResponse" in str(e):
                    st.warning(f"No {amenity_type} amenities found within the specified distance.")
                    return
                else:
                    raise e  # If it's a different exception, re-raise it

            # Add markers to the map for valid geometries
            add_markers_to_map(m, amenities, amenity_type)

            # Display the map in Streamlit
            folium_static(m)

    with tab2:
        smart_economy_entities = [
            'POI', 'amenity=marketplace', 'amenity=vending_machine', 'building=commercial', 
            'man_made=offshore_platform', 'man_made=petroleum_well', 'man_made=pipeline', 'man_made=works', 'office= company',
            'office=coworking', 'shop=all', 'tourism=alpine_hut', 'tourism=attraction', 'tourism=camp_pitch', 'tourism=camp_site',
            'tourism=caravan_site', 'building=chalet', 'building=guest_house', 'building=hostel', 'building=hotel', 'tourism=information',
            'tourism motel', 'building=museum', 'tourism=wilderness_hut'
        ]
        
        selected_entity = st.selectbox("Select Entity Type:", smart_economy_entities, key='smart_economy_entity')
        
        if st.button('Show Selected Entities', key='t2'):
            try:
                entities = get_smart_entities(lat, lon, selected_entity, RADIUS)
            except Exception as e:
                st.error("An error occurred while fetching entities.")
                st.error(e)
                return

            add_markers_to_map(m, entities, selected_entity)

            folium_static(m)
            
    with tab3:  # SmartGovernance tab
        smart_governance_entities = ['amenity=townhall', 'amenity=courthouse', 'amenity=police', 'amenity=fire_station', 'building=government']  # replace with actual entity types
        selected_entity2 = st.selectbox("Select Entity Type:", smart_governance_entities, key='smart_governance_entity')

        if st.button('Show Entities', key='entity'):
            try:
                entities = get_smart_entities(lat, lon, selected_entity2, RADIUS)
            except Exception as e:
                st.error("An error occurred while fetching entities.")
                st.error(e)
                return

            add_markers_to_map(m, entities, selected_entity2)

            folium_static(m)
            
    with tab4:
        smart_mobility_entities = [
            'barrier=bump_gate',
            'barrier=bus_trap',
            'barrier=cycle_barrier',
            'barrier=motorcycle_barrier',
            'barrier=sump_buster',
            'building=train_station',
            'building=transportation',
            'building=parking',
            'highway=motorway',
            'public_transport=all',
            'railway=all',
            'route=all'
        ]   
        
        selected_entity3 = st.selectbox("Select Entity Type:", smart_mobility_entities, key='smart_mobility_entity')
        
        if st.button('Show Selected Entities', key='t4'):
            try:
                entities = get_smart_entities(lat, lon, selected_entity3, RADIUS)
            except Exception as e:
                st.error("An error occurred while fetching entities.")
                st.error(e)
                return

            add_markers_to_map(m, entities, selected_entity3)

            folium_static(m)
            
    with tab5:
        smart_environment_entities = [
            "amenity=recycling",
            "boundary=forest",
            "boundary=forest_compartment",
            "boundary=hazard",
            "boundary=national_park",
            "boundary=protected_area",
            "leisure=garden", 
            "leisure=nature_reserve", 
            "leisure=park", 
            "man_made=gasometer",
            "man_made=mineshaft",
            "man_made=wastewater_plant",
            "man_made=water_works",
            "natural=grass",
            "water=river"
        ]
  
        selected_entity5 = st.selectbox("Select Entity Type:", smart_environment_entities, key='smart_environment_entity')
        
        if st.button('Show Selected Entities', key='t5'):
            try:
                entities = get_smart_entities(lat, lon, selected_entity5, RADIUS)
            except Exception as e:
                st.error("An error occurred while fetching entities.")
                st.error(e)
                return

            add_markers_to_map(m, entities, selected_entity5)

            folium_static(m)
            
    with tab6:
        smart_people_entities = [    # General Educational Facilities
            "amenity=college",
            "amenity=kindergarten",
            "amenity=school",
            "amenity=university",
            "office=educational_institution",
            "office=employment_agency",
            "amenity=refugee_site"
        ]  
        
        selected_entity6 = st.selectbox("Select Entity Type:", smart_people_entities, key='smart_people_entity')
        
        if st.button('Show Selected Entities', key='t6'):
            try:
                entities = get_smart_entities(lat, lon, selected_entity6, RADIUS)
            except Exception as e:
                st.error("An error occurred while fetching entities.")
                st.error(e)
                return

            add_markers_to_map(m, entities, selected_entity6)

            folium_static(m)
            
    with tab7:
        smart_living_entities = [
                "amenity=internet_cafe",
                "amenity=public_bath",
                "amenity=vending_machine",
                "amenity=water_point",
                "amenity=hospital",
                "amenity=museum",
                "amenity=place_of_worship",
                "amenity=fire_station",
                "amenity=toilets",
        ] 
        
        selected_entity7 = st.selectbox("Select Entity Type:", smart_living_entities, key='smart_living_entity')
        
        if st.button('Show Selected Entities', key='t7'):
            try:
                entities = get_smart_entities(lat, lon, selected_entity7, RADIUS)
            except Exception as e:
                st.error("An error occurred while fetching entities.")
                st.error(e)
                return

            add_markers_to_map(m, entities, selected_entity7)

            folium_static(m)
    
    # Add a button to count amenities
    if st.button('Count Amenities'):
        amenities_count = count_amenities(lat, lon, RADIUS) 
        st.write('Amenities count within the area:')
        st.write(amenities_count)
        text_area = st.text_area('AI analysis:', 'Your list provides a good snapshot of the facilities available, but it does not fully capture the technological integration and sustainability aspects that are crucial in defining a village as "smart". While the village seems well-equipped in terms of basic and some advanced amenities, additional information about its technological integration and sustainability initiatives would be necessary to accurately determine its degree of smartness.', height=300)

if __name__ == "__main__":
    main()