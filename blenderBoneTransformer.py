import bpy
import threading
import socketio
import time
import queue
import math
import mathutils

armature_name = 'Armature' 
left_arm_name = 'mixamorig:LeftArm'  # Replace with your second bone name
right_arm_name = 'mixamorig:RightArm'  # Replace with your second bone name
left_shoulder_name = 'mixamorig:LeftShoulder'  # Replace with your first bone name
right_shoulder_name = 'mixamorig:RightShoulder'  # Replace with your first bone name
hips_bone = 'mixamorig:Hips'

axis_indices = {
    "X": 0,
    "Y": 1,
    "Z": 2,
}

def reset_bone_rotation(pose_bone):
        pose_bone.rotation_euler[0] =0
        pose_bone.rotation_euler[1] =0
        pose_bone.rotation_euler[2] =0
        bpy.context.view_layer.update()

def get_pose_bone(armature_name, bone_name):
     # Get the armature object
    arm_obj = bpy.data.objects[armature_name]
    
    # Ensure we're in pose mode
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='POSE')

    # Get the pose bone
    pose_bone = arm_obj.pose.bones[bone_name]
    return pose_bone

 #? NOTE: don't remove this function maybe will be needed
 
def draw_custom_axis(custom_axis,name =  "CustomAxis" ):
      # Create a cone to visualize the custom axis
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.05, depth=1, location=mathutils.Vector((0, 0, 0)))
    cone = bpy.context.object
    cone.name = name
    
    # Set the orientation to align with the custom axis
    custom_axis.normalize()
    rotation_quat = custom_axis.to_track_quat('Z', 'Y')
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
    world_x, world_y, world_z = get_bone_world_axes(armature_name,bone_name)
    draw_custom_axis(world_x,'world_x')
    draw_custom_axis(world_y,'world_y')
    draw_custom_axis(world_z,'world_z')
    
def animate_3_axis_limb(armature_name,arm_bone_name,arm_bone_degree_angles):
    code = arm_bone_degree_angles['code']
    # print(code)
    exec(code)


def animate_with_arduino_data(arduino_data):
        left_arm_bone_data = {}
        right_arm_bone_data = {}
        left_leg_bone_data = {}
        right_leg_bone_data = {}

        selected_armature = bpy.data.objects[armature_name]
        
        for bone_name_and_axis, bone_axis_degree_angle in arduino_data.items():
            bone_name, bone_axis = bone_name_and_axis.split(".")[-2:]

            if bone_name not in selected_armature.pose.bones:
                continue
            selected_bone_in_pose_mode = selected_armature.pose.bones[bone_name]
            if bone_name == "mixamorig:LeftArm":
                left_arm_bone_data[bone_axis] = bone_axis_degree_angle
            elif bone_name == "mixamorig:RightArm":
                right_arm_bone_data[bone_axis] = bone_axis_degree_angle
            if bone_name == "mixamorig:LeftUpLeg":
                left_leg_bone_data[bone_axis] = bone_axis_degree_angle
            elif bone_name == "mixamorig:RightUpLeg":
                right_leg_bone_data[bone_axis] = bone_axis_degree_angle
            elif bone_axis != "code" :
                selected_bone_in_pose_mode.rotation_mode = "XYZ"
                selected_bone_in_pose_mode.rotation_euler[
                    axis_indices[bone_axis]
                ] = math.radians(bone_axis_degree_angle)

        is_to_animate_left_arm = all( key in left_arm_bone_data for key in ["X", "Y", "Z",'code'])
        is_to_animate_left_leg = all( key in left_leg_bone_data for key in ["X", "Y", "Z",'code'])
        is_to_animate_right_arm = all( key in right_arm_bone_data for key in ["X", "Y", "Z",'code'])
        is_to_animate_right_leg = all( key in right_leg_bone_data for key in ["X", "Y", "Z",'code'])
        # print({is_to_animate_left_arm:is_to_animate_left_arm ,left_arm_bone_data:left_arm_bone_data })
        # print('left_arm_bone_data',left_arm_bone_data)
        # print('right_arm_bone_data',right_arm_bone_data)
        if is_to_animate_left_arm:
            animate_3_axis_limb(
                armature_name, "mixamorig:LeftArm", left_arm_bone_data
            )

        if is_to_animate_right_arm:
            animate_3_axis_limb(
                armature_name, "mixamorig:RightArm", right_arm_bone_data
            )
        if is_to_animate_left_leg:
            animate_3_axis_limb(
                armature_name, "mixamorig:LeftUpLeg", left_leg_bone_data
            )

        if is_to_animate_right_leg:
            animate_3_axis_limb(
                armature_name, "mixamorig:RightUpLeg", right_leg_bone_data
            )
  