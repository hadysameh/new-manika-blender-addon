import bpy
import threading
import socketio
import time
import queue
import math
import mathutils


axis_indices = {
    "X": 0,
    "Y": 1,
    "Z": 2,
}


def reset_bone_rotation(pose_bone):
    pose_bone.rotation_euler[0] = 0
    pose_bone.rotation_euler[1] = 0
    pose_bone.rotation_euler[2] = 0
    bpy.context.view_layer.update()


def get_pose_bone(armature_name, bone_name):
    # Get the armature object
    arm_obj = bpy.data.objects[armature_name]

    # Ensure we're in pose mode
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode="POSE")

    # Get the pose bone
    pose_bone = arm_obj.pose.bones[bone_name]
    return pose_bone


# ? NOTE: don't remove this function maybe will be needed
def draw_custom_axis(custom_axis, name="CustomAxis"):
    # Create a cone to visualize the custom axis
    bpy.ops.mesh.primitive_cone_add(
        vertices=16, radius1=0.05, depth=1, location=mathutils.Vector((0, 0, 0))
    )
    cone = bpy.context.object
    cone.name = name

    # Set the orientation to align with the custom axis
    custom_axis.normalize()
    rotation_quat = custom_axis.to_track_quat("Z", "Y")
    cone.rotation_euler = rotation_quat.to_euler()


def get_bone_axes(armature_name, bone_name):
    """
    Extracts the local axes (X, Y, Z) of a bone from its transformation matrix.

    Parameters:
    - armature_name: str, name of the armature object.
    - bone_name: str, name of the bone.

    Returns:
    - tuple of Vectors: (local_x, local_y, local_z)
    """
    # Get the armature object and the pose bone
    armature = bpy.data.objects[armature_name]
    pose_bone = armature.pose.bones[bone_name]

    # Get the bone's transformation matrix in local space
    matrix = pose_bone.matrix

    # Extract the local axes
    local_x = matrix.col[0].xyz  # X-axis (1st column)
    local_y = matrix.col[1].xyz  # Y-axis (2nd column)
    local_z = matrix.col[2].xyz  # Z-axis (3rd column)

    return local_x, local_y, local_z


def get_bone_global_axes(armature_name, bone_name):

    # Get the armature object and the pose bone
    armature = bpy.data.objects[armature_name]
    pose_bone = armature.pose.bones[bone_name]
    global_bone_matrix = armature.matrix_world @ pose_bone.matrix
    bpy.context.view_layer.update()

    # Extract the axes (columns of the rotation part of the matrix)
    global_x_axis = global_bone_matrix.to_3x3()[0]
    global_y_axis = global_bone_matrix.to_3x3()[1]
    global_z_axis = global_bone_matrix.to_3x3()[2]

    return global_x_axis, global_y_axis, global_z_axis


def get_bone_world_axes(armature_name, bone_name):
    armature = bpy.data.objects[armature_name]
    pose_bone = armature.pose.bones[bone_name]

    global_matrix = armature.matrix_world @ pose_bone.matrix

    # Extract global axes from the matrix
    world_x_axis = global_matrix.to_3x3()[0]  # Global X axis
    world_y_axis = global_matrix.to_3x3()[1]  # Global Y axis
    world_z_axis = global_matrix.to_3x3()[2]  # Global Z axis

    return world_x_axis, world_y_axis, world_z_axis


def draw_bone_world_axes(armature_name, bone_name):
    world_x, world_y, world_z = get_bone_world_axes(armature_name, bone_name)
    draw_custom_axis(world_x, "world_x")
    draw_custom_axis(world_y, "world_y")
    draw_custom_axis(world_z, "world_z")


def animate_3_axis_limb(armature_name, arm_bone_name, arm_bone_degree_angles):
    code = arm_bone_degree_angles["code"]
    # print(code)
    exec(code)


def animate_with_arduino_data(arduino_data):
    for bone_name, bone_code in arduino_data.items():
        exec(bone_code)
