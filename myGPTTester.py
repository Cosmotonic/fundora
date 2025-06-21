





import folium

# Create base map centered on Iceland
iceland_map = folium.Map(location=[64.9631, -19.0208], zoom_start=6)

# Define stops based on the provided itinerary
stops = [
    (64.0164, -22.6056, "Day 1: Keflavík – Arrival & Welcome Dinner"),
    (64.2550, -21.1300, "Day 2: Þingvellir – Golden Circle Start"),
    (64.3136, -20.3024, "Day 2: Geysir"),
    (64.3275, -20.1218, "Day 2: Gullfoss Waterfall"),
    (63.5615, -20.3022, "Day 2: Seljalandsfoss"),
    (63.5321, -19.5119, "Day 2: Skógafoss"),
    (63.4045, -19.0450, "Day 3: Reynisfjara – Black Sand Beach"),
    (64.0484, -16.1794, "Day 3: Jökulsárlón – Glacier Lagoon"),
    (65.2663, -14.3948, "Day 4: Egilsstaðir – Thermal Pools"),
    (65.8145, -16.5055, "Day 5: Dettifoss – Powerful Waterfall"),
    (66.0110, -16.5050, "Day 5: Ásbyrgi Canyon – Trekking"),
    (66.0449, -17.3389, "Day 6: Húsavík – Whale Watching"),
    (65.6839, -18.1105, "Day 6: Goðafoss – Waterfall of the Gods"),
    (65.3865, -20.1286, "Day 7: Hvammstangi – Travel Day"),
    (64.1355, -21.8954, "Day 8: Reykjavik – Relax & Thermal Pools"),
    (64.0164, -22.6056, "Day 9: Keflavík – Departure"),
]

# Add markers to the map
for lat, lon, label in stops:
    folium.Marker(location=[lat, lon], popup=label).add_to(iceland_map)

# Draw route line
folium.PolyLine([(lat, lon) for lat, lon, _ in stops], color="blue", weight=3).add_to(iceland_map)

# Display the map
iceland_map
