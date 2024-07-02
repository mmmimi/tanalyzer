import streamlit as st
import osmnx as ox
import folium
import requests
import json
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
    "FTA (Darja), Slovenia": (46.5530, 15.6509),
    "Arpavon, France": (44.370914993, 5.27351034083),
    "Aubres, France": (44.3893044332, 5.1543771035),
    "Aulan, France": (44.2300209805, 5.42219540267),
    "Ballons, France": (44.2517233325, 5.64403556412),
    "Barret-de-Lioure, France": (44.1754211867, 5.51622125908),
    "Beauvoisin, France": (44.3007007366, 5.2126241299),
    "Bellecombe-Tarendol, France": (44.3570805263, 5.35605853142),
    "Benivay-Ollon, France": (44.3110239354, 5.18792865009),
    "Bésignan, France": (44.320135403, 5.32102321882),
    "Buis-les-Baronnies, France": (44.276084918, 5.27102720538),
    "Châteauneuf-de-Bordette, France": (44.3367876244, 5.17129087386),
    "Chaudebonne, France": (44.4749699502, 5.23878850401),
    "Chauvac-Laux-Montaux, France": (44.3222598989, 5.53474260728),
    "Condorcet, France": (44.4150216526, 5.17856915513),
    "Cornillac, France": (44.4397962744, 5.40427048802),
    "Cornillon-sur-l’Oule, France": (44.4553268167, 5.36026006175),
    "Curnier, France": (44.387658631, 5.23421106174),
    "Eygalayes, France": (44.2211440236, 5.59423968429),
    "Eygaliers, France": (44.2403379768, 5.28466764247),
    "Eyroles, France": (44.417094329, 5.24106129822),
    "Izon-la-Bruisse, France": (44.2626520875, 5.60226769891),
    "La Charce, France": (44.4668723535, 5.44466918876),
    "La Penne-sur-l’Ouvèze, France": (44.2503681815, 5.23252395755),
    "La Roche-sur-le-Buis, France": (44.2625812469, 5.34101183886),
    "La Rochette-du-Buis, France": (44.2610706065, 5.42166701119),
    "Le Poët-en-Percip, France": (44.2484174261, 5.39418333523),
    "Le Poët-Sigillat, France": (44.3631938216, 5.31860156663),
    "Lemps, France": (45.0972922386, 4.778993534),
    "Les Pilles, France": (44.3778726864, 5.19915828289),
    "Mérindol-les-Oliviers, France": (44.2725055479, 5.1684408091),
    "Mévouillon, France": (44.2346171686, 5.47885128912),
    "Mirabel-aux-Baronnies, France": (44.3146283758, 5.10177171848),
    "Montauban-sur-l’Ouvèze, France": (44.2773478714, 5.51851244253),
    "Montaulieu, France": (44.3578984951, 5.21799658575),
    "Montbrun-les-Bains, France": (44.1877148289, 5.43426917221),
    "Montferrand-la-Fare, France": (44.3419027323, 5.44998013402),
    "Montguers, France": (44.301845332, 5.47245831893),
    "Montréal-les-Sources, France": (44.4006997235, 5.30675272365),
    "Nyons, France": (44.3564879814, 5.12880832),
    "Pelonne, France": (44.3822334481, 5.38062257159),
    "Piegon, France": (44.298616176, 5.12425949306),
    "Pierrelongue, France": (44.2495510618, 5.21417355869),
    "Plaisians, France": (44.2251384838, 5.337199685),
    "Pommerol, France": (44.4372174843, 5.46497895783),
    "Propiac, France": (44.276584707, 5.20940872423),
    "Reilhanette, France": (44.1712233115, 5.40493973585),
    "Remuzat, France": (44.4038075452, 5.35604206561),
    "Rioms, France": (44.4038075452, 5.35604206561),
    "Rochebrune, France": (44.3264290154, 5.23698675047),
    "Roussieux, France": (44.3315645396, 5.47886581658),
    "Sahune, France": (44.4062765625, 5.27186320127),
    "Saint-Auban-sur-l’Ouvèze, France": (44.2973942019, 5.43012241748),
    "Saint-Ferréol-Trente-Pas, France": (44.4418058243, 5.22377937288),
    "Saint-Maurice-sur-Eygues, France": (44.3029325431, 5.00596735706),
    "Saint-May, France": (44.4246891734, 5.32934515143),
    "Saint-Sauveur-Gouvernet, France": (44.3303880901, 5.37614176075),
    "Sainte-Euphémie-sur-Ouvèze, France": (44.3011387229, 5.3913641468),
    "Sainte-Jalle, France": (44.3334508898, 5.27890908641),
    "Sederon, France": (44.1975046499, 5.55416093649),
    "Valouse, France": (44.4594883519, 5.19108928218),
    "Venterol, France": (44.3977805769, 5.09846513358),
    "Verclause, France": (44.3954497171, 5.40735314381),
    "Vercoiran, France": (44.2937794965, 5.35057643289),
    "Vers-sur-Méouge, France": (44.2358606593, 5.55110208603),
    "Villefranche-le-Château, France": (44.2152597669, 5.50831127895),
    "Villeperdrix, France": (44.4557494791, 5.29971413853),
    "Vinsobres, France": (44.3356176138, 5.0506163995)
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
    
    if st.button('AI Analysis'):
        # Execute the existing code to count amenities
        amenities_count = count_amenities(lat, lon, 1000)
        st.write('Amenities count within the area:')
        st.write(amenities_count)
        
        # Construct the message with the dynamic amenities_count
        message_content = f"What is the degree of digitalization of a village located in a rural territory with these facilities: {amenities_count}? What can we do to improve it?"

        # API request setup
        url = 'https://www.chatbase.co/api/v1/chat'
        headers = {
            'Authorization': 'Bearer d1a408c0-5e75-40ca-99e5-424e830d26ed',
            'Content-Type': 'application/json'
        }
        data = {
            "messages": [
                {"content": message_content, "role": "user"}
            ],
            "chatbotId": "X5mqGdkfYYzpPO2R7Q5Jv",
            "stream": False,
            "temperature": 0
        }
        
        # Make the API call
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Process the API response
        if response.status_code == 200:
            json_data = response.json()
            response_text = json_data.get('text', 'No text in response')
            st.write("Response:", response_text)
        else:
            error_message = response.json().get('message', 'Unknown error')
            st.write('Error:', error_message)

if __name__ == "__main__":
    main()