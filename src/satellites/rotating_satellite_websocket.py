import asyncio
import websockets
import math
import json






# Define parameters for multiple objects
# objects = {
#     "object1": {"axis": (1, 0, 0), "speed": 1, "radius": 1.2, "initial_point": (0, 1.2, 0)},
#     "object2": {"axis": (0, 1, 0), "speed": 1, "radius": 1.2, "initial_point": (1.2, 0, 0)},
#     "object3": {"axis": (0, 0, 1), "speed": 1, "radius": 1.2, "initial_point": (1.2, 0, 0)},
#     "object4": {"axis": (1, 0, 0), "speed": 1, "radius": 1.2, "initial_point": (0, 1.4, 0)},
#     "object5": {"axis": (0, 1, 0), "speed": 1, "radius": 1.2, "initial_point": (1.4, 0, 0)},
#     "object6": {"axis": (0, 0, 1), "speed": 1, "radius": 1.2, "initial_point": (1.4, 0, 0)},
#     "object7": {"axis": (1, 0, 0), "speed": 1, "radius": 1.2, "initial_point": (0, 1.6, 0)},
#     "object8": {"axis": (0, 1, 0), "speed": 1, "radius": 1.2, "initial_point": (1.6, 0, 0)},
#     "object9": {"axis": (0, 0, 1), "speed": 1, "radius": 1.2, "initial_point": (1.6, 0, 0)},
#     # Add more objects as needed
# }

# objects = {'satellite1': {'axis': (0, -0.8098431587894976, 0), 'speed': 1.4772755742432762, 'radius': 1.2, 'initial_point': (-1.6268127701081738, 1.7449073894341436, 0.9900897724823161)}, 'satellite2': {'axis': (0, 0.8904858155672402, 0), 'speed': 0.8074818980085756, 'radius': 1.2, 'initial_point': (0.241732639818117, 0.8277227572730346, 1.092328688127847)}, 'satellite3': {'axis': (0, 0.7763429820962686, 0), 'speed': 1.2572358906739223, 'radius': 1.2, 'initial_point': (-0.7845655704062033, -0.1085266629345405, 1.7527004032135292)}, 'satellite4': {'axis': (0, 0.0798792564786428, 0), 'speed': 0.8713712831379535, 'radius': 1.2, 'initial_point': (1.825648734943563, 0.26754746106726923, -0.6201150429347355)}, 'satellite5': {'axis': (0, 0.18195120849578683, 0), 'speed': 0.7188082899611309, 'radius': 1.2, 'initial_point': (-1.5898099815836955, 1.521390565392359, 0.7535548233109801)}, 'satellite6': {
#     'axis': (0, 0.18943477446672596, 0), 'speed': 1.3907271586764862, 'radius': 1.2, 'initial_point': (-1.3983876262279789, 0.8372518041110961, -0.012083289979479606)}, 'satellite7': {'axis': (0, 0.05126010722909724, 0), 'speed': 0.5005565629620772, 'radius': 1.2, 'initial_point': (0.3221023810328485, -0.8467454519438635, -1.6520377153503527)}, 'satellite8': {'axis': (0, 0.18662652752835585, 0), 'speed': 0.8288465695618286, 'radius': 1.2, 'initial_point': (0.26764978822151253, 0.31142938691365174, 1.2046781789294267)}, 'satellite9': {'axis': (0, 0.9601002934686558, 0), 'speed': 1.2285998362674708, 'radius': 1.2, 'initial_point': (1.0845317434609592, 1.4381914268575517, -1.0578519241314668)}, 'satellite10': {'axis': (0, 0.15728381878052944, 0), 'speed': 1.0770983523001427, 'radius': 1.2, 'initial_point': (0.6461381871220451, -0.5050257739759019, -0.9319020051277596)}}



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
