bl_info = {
    "name": "Bone Rotation Control",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Bone Rotation Control",
    "description": "Control the rotational angle of a bone",
    "category": "3D View",
}

import bpy
from .blenderSocketScript import classes 

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()
