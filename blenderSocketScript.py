import bpy
import threading
import socketio
import time
import queue
import math
import mathutils
from .blenderBoneTransformer import animate_with_arduino_data
# Global variables to manage the Socket.IO client and thread
sio = None
socket_thread = None
stop_thread = False
data_queue = queue.Queue()
 

def start_socketio_client():
    """
    Starts the Socket.IO client in a separate thread.
    """
    global sio, stop_thread

    def socketio_handler():
        global stop_thread
        sio = socketio.Client()

        @sio.event
        def connect():
            print("Socket.IO connected.")

        @sio.on('arduinoData')
        def handle_arduino_data(data):
                data_queue.put(data)
        
        @sio.event
        def disconnect():
            print("Socket.IO disconnected.")

        try:
            # Replace with your Socket.IO server URL
            sio.connect("http://localhost:3000")
            print("Socket.IO client connected.")
            while not stop_thread:
                sio.sleep(0.1)  # Keep the connection alive
        except Exception as e:
            print(f"Error in Socket.IO: {e}")
        finally:
            if sio.connected:
                sio.disconnect()
            print("Socket.IO thread stopped.")

    # Start the Socket.IO client thread
    stop_thread = False
    socket_thread = threading.Thread(target=socketio_handler, daemon=True)
    socket_thread.start()

def stop_socketio_client():
    """
    Stops the Socket.IO client and the thread.
    """
    global stop_thread, socket_thread, sio

    if sio and sio.connected:
        try:
            sio.disconnect()
            print("Socket.IO client disconnected.")
        except Exception as e:
            print(f"Error while disconnecting: {e}")

    # Signal the thread to stop
    stop_thread = True

    if socket_thread and socket_thread.is_alive():
        socket_thread.join(timeout=2)  # Allow up to 2 seconds to terminate
        if socket_thread.is_alive():
            print("Socket.IO thread did not stop properly.")
        else:
            print("Socket.IO thread stopped.")


# UI Panel for Start/Stop Buttons
class SOCKETIO_PT_Panel(bpy.types.Panel):
    bl_label = "Socket.IO Control Panel"
    bl_idname = "SOCKETIO_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Socket.IO"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("socketio.start", text="Start Socket.IO")
        col.operator("socketio.stop", text="Stop Socket.IO")

# Operators to Start/Stop Socket.IO
class SOCKETIO_OT_Start(bpy.types.Operator):
    bl_idname = "socketio.start"
    bl_label = "Start Socket.IO Client"

    def execute(self, context):
        start_socketio_client()
        self.report({'INFO'}, "Socket.IO client started.")
        return {'FINISHED'}

class SOCKETIO_OT_Stop(bpy.types.Operator):
    bl_idname = "socketio.stop"
    bl_label = "Stop Socket.IO Client"

    def execute(self, context):
        stop_socketio_client()
        self.report({'INFO'}, "Socket.IO client stopped.")
        return {'FINISHED'}

# Register/Unregister Classes
classes = [SOCKETIO_PT_Panel, SOCKETIO_OT_Start, SOCKETIO_OT_Stop]


def process_queue():
    while not data_queue.empty():
        try:
            data = data_queue.get_nowait()
            animate_with_arduino_data(data)
        except queue.Empty:
            print('error in arduino data')
            pass
    # Schedule the next run
    return 0.25  # Run this function again in 1 second

bpy.app.timers.register(process_queue)
