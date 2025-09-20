from shapely.geometry import Point, Polygon
from shapely.validation import explain_validity
import matplotlib.pyplot as plt

# Define the zones (lon, lat)
zones = [
    {
        "name": "RED",
        "priority": 3,
        "polygon": Polygon([
            (88.45294, 22.98805),
            (88.45321, 22.98799),
            (88.45361, 22.98892),
            (88.45332, 22.98902),
            (88.45294, 22.98805)  
        ])
    },
    {
        "name": "GREEN",
        "priority": 2,
        "polygon": Polygon([
            (88.45272, 22.98816),
            (88.45285, 22.9881),
            (88.45323, 22.98905),
            (88.45309, 22.9891),
            (88.45272, 22.98816)  
        ])
    },
    {
        "name": "YELLOW",
        "priority": 1,
        "polygon": Polygon([
            (88.45285, 22.9881),
            (88.45295, 22.98808),
            (88.45332, 22.98902),
            (88.45323, 22.98905),
            (88.45285, 22.9881)  
        ])
    }
]

# Validate polygons
for zone in zones:
    if not zone["polygon"].is_valid:
        print(f"Fixing polygon for {zone['name']}: {explain_validity(zone['polygon'])}")
        zone["polygon"] = zone["polygon"].buffer(0)  # fixes self-intersections

def detect_zone(lat, lon):
    """
    Check which zone a given coordinate belongs to.
    Input: latitude, longitude
    """
    point = Point(lon, lat)
    matched = []

    for zone in zones:
        poly = zone["polygon"]
        if poly.contains(point) or poly.touches(point):
            matched.append(zone)

    if not matched:
        return None
    return max(matched, key=lambda z: z["priority"])["name"]

def plot_zones(lat=None, lon=None):
    """
    Plot polygons and optionally the input point.
    """
    fig, ax = plt.subplots()

    colors = {"RED": "red", "GREEN": "green", "YELLOW": "yellow"}

    # Plot polygons
    for zone in zones:
        x, y = zone["polygon"].exterior.xy
        ax.fill(x, y, alpha=0.3, fc=colors[zone["name"]], ec="black", label=zone["name"])

    # Plot point
    if lat and lon:
        ax.plot(lon, lat, "bo", markersize=10, label="Your Location")

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Zone Map")
    ax.legend()
    plt.show()

if __name__ == "__main__":
    print("Zone checker running... Enter coordinates one by one.")
    print("Priority: RED > GREEN > YELLOW")
    print("Press CTRL+C to stop\n")

    while True:
        try:
            lat_raw = input("Enter latitude : ").strip()
            lon_raw = input("Enter longitude: ").strip()

            if not lat_raw or not lon_raw:
                print("Both latitude and longitude are required.")
                continue

            lat, lon = map(float, (lat_raw, lon_raw))
            zone = detect_zone(lat, lon)

            if zone:
                print(f"You are in the {zone} zone\n")
            else:
                print("You are in SAFE zone (outside all polygons)\n")

            # Show map for visual confirmation
            plot_zones(lat, lon)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}\n")
        