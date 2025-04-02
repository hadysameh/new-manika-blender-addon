import bpy
import threading
import socketio
import time
import queue
import math
import mathutils

selected_armature = bpy.data.objects["Armature"]
shoulder_bone_in_pose_mode = selected_armature.pose.bones["Ctrl_Arm_FK_Left"]
if shoulder_bone_in_pose_mode:
    x = math.radians(13)
    y = math.radians(-53)
    z = math.radians(0)
    shoulder_bone_in_pose_mode.rotation_mode = "XYZ"  # Enforce gimbal lock
    bpy.context.view_layer.update()

    shoulder_bone_in_pose_mode.rotation_euler = mathutils.Euler((x, y, z), "XYZ")
    bpy.context.view_layer.update()
    #  ============================================================
    modify_y = math.radians(-90)
    # Convert current rotation to matrix
    bone_matrix = shoulder_bone_in_pose_mode.matrix
    # Create a rotation matrix for local Y axis
    local_y_rotation = mathutils.Matrix.Rotation(
        modify_y, 4, shoulder_bone_in_pose_mode.y_axis
    )
    # Apply new rotation by multiplying the local rotation
    shoulder_bone_in_pose_mode.matrix = local_y_rotation @ bone_matrix
    bpy.context.view_layer.update()
