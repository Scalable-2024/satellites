import asyncio
import websockets
import math
import json

# Define parameters for multiple objects
objects = {
    "object1": {"axis": (1, 0, 0), "speed": 1, "radius": 1.2, "initial_point": (0, 1.2, 0)},
    "object2": {"axis": (0, 1, 0), "speed": 1, "radius": 1.2, "initial_point": (1.2, 0, 0)},
    "object3": {"axis": (0, 0, 1), "speed": 1, "radius": 1.2, "initial_point": (1.2, 0, 0)},
    # Add more objects as needed
}


def rotate_point(point, axis, angle):
    """Rotate point around given axis by the angle using Rodrigues' rotation formula."""
    ux, uy, uz = axis
    x, y, z = point
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    rotated_x = (cos_theta + ux**2 * (1 - cos_theta)) * x + \
                (ux * uy * (1 - cos_theta) - uz * sin_theta) * y + \
                (ux * uz * (1 - cos_theta) + uy * sin_theta) * z

    rotated_y = (uy * ux * (1 - cos_theta) + uz * sin_theta) * x + \
                (cos_theta + uy**2 * (1 - cos_theta)) * y + \
                (uy * uz * (1 - cos_theta) - ux * sin_theta) * z

    rotated_z = (uz * ux * (1 - cos_theta) - uy * sin_theta) * x + \
                (uz * uy * (1 - cos_theta) + ux * sin_theta) * y + \
                (cos_theta + uz**2 * (1 - cos_theta)) * z

    return rotated_x, rotated_y, rotated_z


async def send_coordinates(websocket):
    """Send coordinates for all objects to the connected client."""
    angles = {obj: 0 for obj in objects}  # Initialize angles for all objects

    while True:
        result = {}
        for obj_name, params in objects.items():
            axis = params["axis"]
            speed = params["speed"]
            radius = params["radius"]

            # Scale initial point to radius
            initial_point = params["initial_point"]

            # Rotate point based on the current angle
            x, y, z = rotate_point(initial_point, axis, angles[obj_name])
            result[obj_name] = {"x": x, "y": y, "z": z}

            # Increment angle for the next iteration
            angles[obj_name] += speed * 0.05

        # Send all object coordinates as a single JSON object
        await websocket.send(json.dumps(result))

        # Wait before sending the next update
        await asyncio.sleep(0.1)  # 100ms update interval


async def handler(websocket):
    """Handle incoming WebSocket connections."""
    try:
        await send_coordinates(websocket)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")


async def main():
    """Main function to run the WebSocket server."""
    async with websockets.serve(handler, "localhost", 8765):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
