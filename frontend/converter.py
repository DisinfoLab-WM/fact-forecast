import json

# Load your original GeoJSON file
with open('ne_110m_admin_0_countries.json', 'r') as f:
    geojson = json.load(f)

# Create a new FeatureCollection
feature_collection = {
    "type": "FeatureCollection",
    "features": []
}

# Loop through each geometry in the GeometryCollection and convert it to a feature
for index, geometry in enumerate(geojson['geometries']):
    feature = {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "id": index + 1,  # You can set a custom ID or other properties if needed
            "name": f"Geometry {index + 1}"
        }
    }

    # Add the feature to the FeatureCollection
    feature_collection["features"].append(feature)

# Write the new FeatureCollection to a new file
with open('converted_geojson.json', 'w') as f:
    json.dump(feature_collection, f, indent=2)

print("Conversion successful! The new GeoJSON file has been created.")
