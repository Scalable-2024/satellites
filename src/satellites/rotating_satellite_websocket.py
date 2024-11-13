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


objects = {'satellite1': {'axis': (0, 0.3954558228562166, 0), 'speed': 1.0118776132068572, 'radius': 1.2, 'initial_point': (0.6168463043354713, 1.9017278404967266, 0.26926249629769305)}, 'satellite2': {'axis': (0, -0.330595693112155, 0), 'speed': 1.1447675702434887, 'radius': 1.2, 'initial_point': (0.6410919259180097, -1.9988309834195168, -1.8340971554833256)}, 'satellite3': {'axis': (0, -0.5407256171363348, 0), 'speed': 0.6249091701171622, 'radius': 1.2, 'initial_point': (1.125936365421635, 1.41349417433646, -1.0580817555770818)}, 'satellite4': {'axis': (0, 0.0645010819727374, 0), 'speed': 0.9345129184606191, 'radius': 1.2, 'initial_point': (-1.8533927954730918, 1.3056907258727204, -0.6271085387133315)}, 'satellite5': {'axis': (0, 0.6017421706271728, 0), 'speed': 1.2473665724314242, 'radius': 1.2, 'initial_point': (-0.9902939679633795, -0.6308107940703667, 1.109221590017229)}, 'satellite6': {'axis': (0, 0.19709613194147146, 0), 'speed': 1.2911388265420558, 'radius': 1.2, 'initial_point': (0.32216942717921304, -1.0519955684494269, 0.853825676357395)}, 'satellite7': {'axis': (0, -0.6519626092521751, 0), 'speed': 1.0642576932504941, 'radius': 1.2, 'initial_point': (0.8282132680203032, -1.553163352245233, 0.4094549340715701)}, 'satellite8': {'axis': (0, -0.20417742842157294, 0), 'speed': 0.9147561058864305, 'radius': 1.2, 'initial_point': (0.7564238819405826, -1.7575548457604522, 1.4832549683557223)}, 'satellite9': {'axis': (0, 0.42822095484828515, 0), 'speed': 0.7879356113920138, 'radius': 1.2, 'initial_point': (0.7174873388905882, 0.8823268287798824, -0.18124451843032707)}, 'satellite10': {'axis': (0, -0.22259822308052768, 0), 'speed': 1.440512059926791, 'radius': 1.2, 'initial_point': (0.6815160399694427, -0.07189703290081262, 0.5096365084556682)},
           'satellite11': {'axis': (0, -0.6664866896289254, 0), 'speed': 1.258903755366024, 'radius': 1.2, 'initial_point': (0.8478681565456267, -1.6259908119918207, 1.0524190730322522)}, 'satellite12': {'axis': (0, -0.671744519955666, 0), 'speed': 0.6927570017689694, 'radius': 1.2, 'initial_point': (0.6771960361852507, 0.36770057084582675, -0.5970422699736462)}, 'satellite13': {'axis': (0, 0.11242710255616295, 0), 'speed': 0.7403184533683607, 'radius': 1.2, 'initial_point': (-0.6944714010615161, -1.8732700973763055, 0.07610414838245827)}, 'satellite14': {'axis': (0, -0.516599036996954, 0), 'speed': 0.8094589030510096, 'radius': 1.2, 'initial_point': (0.930289950629656, 0.8985077076145425, 1.0167237361320303)}, 'satellite15': {'axis': (0, 0.11354897651351803, 0), 'speed': 0.7001252879434615, 'radius': 1.2, 'initial_point': (1.139354403964579, -0.10317379443894614, -1.6130591833424202)}, 'satellite16': {'axis': (0, -0.8831449006751613, 0), 'speed': 0.6985367477709501, 'radius': 1.2, 'initial_point': (0.3594249892097534, -1.403416993699253, 1.744822869884275)}, 'satellite17': {'axis': (0, 0.14566353845945956, 0), 'speed': 1.4899412739222369, 'radius': 1.2, 'initial_point': (1.782410138399261, -0.5980136175035065, -1.8242898996301533)}, 'satellite18': {'axis': (0, 0.8289417342215839, 0), 'speed': 1.2263842668644107, 'radius': 1.2, 'initial_point': (-1.427260733961527, -0.3988515687756409, -0.7802243659873418)}, 'satellite19': {'axis': (0, 0.4358045943476232, 0), 'speed': 1.23692675111806, 'radius': 1.2, 'initial_point': (1.5822408774617203, 1.7248308156867869, 1.2828436561064773)}, 'satellite20': {'axis': (0, 0.16488659080622914, 0), 'speed': 0.8303506569956974, 'radius': 1.2, 'initial_point': (-1.4371674025952963, 0.28343806977833497, 0.9777197786057368)}}

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
