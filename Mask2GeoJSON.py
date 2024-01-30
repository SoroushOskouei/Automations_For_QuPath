import cv2
import numpy as np
import json
import glob
import os



def mask_to_geojson(mask_path, geojson_path, size):
    # Load the binary mask image
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    mask = cv2.resize(mask, (size[1], size[0]))

    # Find the contours of the white areas in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize an empty list to store the GeoJSON features
    features = []

    # Iterate over the contours
    for i, contour in enumerate(contours):
        # Check if the contour is a parent
        if hierarchy[0][i][3] == -1:
            # Get the coordinates of the parent contour
            parent_contour = contour.reshape(-1, 2)

            # Close the parent contour by appending the first point to the end
            parent_contour = np.append(parent_contour, [parent_contour[0]], axis=0)

            # Initialize a list for holes (child contours)
            holes = []

            # Check for child contours
            child = hierarchy[0][i][2]
            while child != -1:
                child_contour = contours[child].reshape(-1, 2)

                # Close the child contour by appending the first point to the end
                child_contour = np.append(child_contour, [child_contour[0]], axis=0)
                
                holes.append([[c[0].item(), c[1].item()] for c in child_contour])
                child = hierarchy[0][child][0]  # Get next child contour

            # Convert the parent contour coordinates to GeoJSON format
            geometry = {
                "type": "Polygon",
                "coordinates": [[[c[0].item(), c[1].item()] for c in parent_contour]] + holes
            }

            # Create a GeoJSON feature for the parent contour
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


files = glob.glob('D:/WSIs/SegmentationResults/*.png')
# print(files)

sizes =[[W0,H0],[W1,H1],...]


for indx, f in enumerate(files):
    print(f)
    root, ext = os.path.splitext(f)
    basename = os.path.basename(root)
    mask_path = f
    geojson_path = "_ClusterBased.json"
    mask_to_geojson(mask_path, './' + basename + geojson_path, [sizes[indx][1], sizes[indx][0]])
