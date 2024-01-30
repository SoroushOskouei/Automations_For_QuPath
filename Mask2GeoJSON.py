import cv2
import numpy as np
import json


def mask_to_geojson(mask_path, geojson_path, resize_factor=(141681/234)):
    # Load the binary mask image
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    
    # Find the contours of the white areas in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize an empty list to store the GeoJSON features
    features = []
    
    # Iterate over the contours
    for contour in contours:
        # Get the coordinates of the contour
        contour = contour.reshape(-1, 2)

        # Resize the contour coordinates
        contour = contour * resize_factor

        # Close the contour by appending the first point to the end of the array
        contour = np.append(contour, [contour[0]], axis=0)
        
        # Convert the contour coordinates to GeoJSON format
        geometry = {
            "type": "Polygon",
            "coordinates": [[[c[0].item(), c[1].item()] for c in contour]]
        }
        
        # Create a GeoJSON feature for the contour
        feature = {
            "type": "Feature",
            "geometry": geometry
        }
        
        # Add the feature to the list of features
        features.append(feature)
    
    # Create the GeoJSON feature collection
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Write the GeoJSON to a file
    with open(geojson_path, "w") as f:
        json.dump(geojson, f)
    print(f"GeoJSON saved to {geojson_path}")

# Example usage:
mask_path = "C:/Users/sorou/OneDrive/Pictures/148.png"
geojson_path = "./148.json"
mask_to_geojson(mask_path, geojson_path)
