import asyncio
import websockets
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class SphereVisualizer:
    def __init__(self):
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Create sphere
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        # Plot sphere with wireframe for better visibility
        self.ax.plot_surface(x, y, z, color='blue', alpha=0.1)
        self.ax.plot_wireframe(x, y, z, color='blue', alpha=0.2)

        # Initial point
        self.point, = self.ax.plot(
            [1], [0], [0], marker='o', color='red', markersize=10, label='Satellite')

        # Setup axes and labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Satellite Position')

        # Set fixed limits
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])

        # Set fixed view
        self.ax.view_init(elev=20, azim=45)

        # Enable grid
        self.ax.grid(True)
        plt.legend()

        self.current_pos = [1, 0, 0]  # Initial position

    def update_position(self, x, y, z):
        """Update the 3D point's position."""
        self.current_pos = [x, y, z]

        # Update point position in plot
        self.point.set_data([x], [y])
        self.point.set_3d_properties([z], 'z')

        # Refresh plot
        plt.pause(0.01)  # Pause briefly to allow for UI update


async def main():
    visualizer = SphereVisualizer()
    plt.ion()  # Enable interactive mode

    print("Attempting to connect to server...")
    while True:
        try:
            async with websockets.connect("ws://localhost:8765") as websocket:
                print("Connected to server!")
                while True:
                    data = await websocket.recv()
                    coords = json.loads(data)
                    print(f"Received: {coords}")  # Debug print

                    # Update visualization with new coordinates
                    visualizer.update_position(
                        coords['x'],
                        coords['y'],
                        coords['z']
                    )

                    await asyncio.sleep(0.01)  # Small delay

        except websockets.exceptions.ConnectionClosed:
            print("Connection lost. Reconnecting...")
            await asyncio.sleep(1)
            continue
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(1)
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
        plt.close('all')
