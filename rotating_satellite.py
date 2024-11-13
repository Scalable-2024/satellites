import asyncio
import websockets
import math
import json

# Rotation parameters
axis = (0, 1.2, 0)  # Rotation around the y-axis
speed = 1  # Radians per second
radius = 1.2  # Sphere radius
initial_point = (radius, 0, 0)  # Start on the x-axis


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
    """Send coordinates to the connected client."""
    angle = 0
    while True:
        x, y, z = rotate_point(initial_point, axis, angle)
        await websocket.send(json.dumps({"x": x, "y": y, "z": z}))
        angle += speed * 0.05  # Increment angle based on speed and time step
        await asyncio.sleep(0.1)  # 50ms update interval


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
