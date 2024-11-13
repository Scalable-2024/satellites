import random


def generate_random_satellites(num_satellites):
    """Generate a dictionary of randomly positioned satellites with a fixed axis and speed."""
    satellites = {}
    for i in range(1, num_satellites + 1):
        # Random initial positions within a certain range
        initial_point = (
            random.uniform(-2, 2),
            random.uniform(-2, 2),
            random.uniform(-2, 2)
        )
        satellites[f"satellite{i}"] = {
            "axis": (0, random.uniform(-1, 1), 0),  # Random y-axis value
            "speed": random.uniform(0.5, 1.5),      # Slightly varied speed
            "radius": 1.2,                         # Fixed radius
            "initial_point": initial_point         # Random position
        }
    # print(satellites)
    return satellites


print(generate_random_satellites(20))
