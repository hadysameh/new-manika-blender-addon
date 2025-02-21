import bpy

# Set source and target rig names
source_rig_name = "Armature"
target_rig_name = "rig"

# Bone mapping dictionary
bone_map = {
    "mixamorig9:Head": "c_head.x",
    "mixamorig9:HeadTop_End": "c_head.x",
    "mixamorig9:Hips": "c_root_master.x",
    "mixamorig9:LeftArm": "c_arm_fk.l",
    "mixamorig9:LeftFoot": "c_foot_fk.l",
    "mixamorig9:LeftForeArm": "c_forearm_fk.l",
    "mixamorig9:LeftHand": "c_hand_fk.l",
    "mixamorig9:LeftHandIndex1": "c_index1.l",
    "mixamorig9:LeftHandIndex2": "c_index2.l",
    "mixamorig9:LeftHandIndex3": "c_index3.l",
    "mixamorig9:LeftHandIndex4": "c_hand_fk.l",
    "mixamorig9:LeftHandMiddle1": "c_middle1.l",
    "mixamorig9:LeftHandMiddle2": "c_middle2.l",
    "mixamorig9:LeftHandMiddle3": "c_middle3.l",
    "mixamorig9:LeftHandMiddle4": "c_hand_fk.l",
    "mixamorig9:LeftHandPinky1": "c_pinky1.l",
    "mixamorig9:LeftHandPinky2": "c_pinky2.l",
    "mixamorig9:LeftHandPinky3": "c_pinky3.l",
    "mixamorig9:LeftHandPinky4": "c_hand_fk.l",
    "mixamorig9:LeftHandRing1": "c_ring1.l",
    "mixamorig9:LeftHandRing2": "c_ring2.l",
    "mixamorig9:LeftHandRing3": "c_ring3.l",
    "mixamorig9:LeftHandRing4": "c_hand_fk.l",
    "mixamorig9:LeftHandThumb1": "c_thumb1.l",
    "mixamorig9:LeftHandThumb2": "c_thumb2.l",
    "mixamorig9:LeftHandThumb3": "c_thumb3.l",
    "mixamorig9:LeftHandThumb4": "c_hand_fk.l",
    "mixamorig9:LeftLeg": "c_leg_fk.l",
    "mixamorig9:LeftShoulder": "c_shoulder.l",
    "mixamorig9:LeftToeBase": "c_toes_fk.l",
    "mixamorig9:LeftToe_End": "c_toes_fk.l",
    "mixamorig9:LeftUpLeg": "c_thigh_fk.l",
    "mixamorig9:Neck": "c_neck.x",
    "mixamorig9:RightArm": "c_arm_fk.r",
    "mixamorig9:RightFoot": "c_foot_fk.r",
    "mixamorig9:RightForeArm": "c_forearm_fk.r",
    "mixamorig9:RightHand": "c_hand_fk.r",
    "mixamorig9:RightHandIndex1": "c_index1.r",
    "mixamorig9:RightHandIndex2": "c_index2.r",
    "mixamorig9:RightHandIndex3": "c_index3.r",
    "mixamorig9:RightHandIndex4": "c_hand_fk.r",
    "mixamorig9:RightHandMiddle1": "c_middle1.r",
    "mixamorig9:RightHandMiddle2": "c_middle2.r",
    "mixamorig9:RightHandMiddle3": "c_middle3.r",
    "mixamorig9:RightHandMiddle4": "c_hand_fk.r",
    "mixamorig9:RightHandPinky1": "c_pinky1.r",
    "mixamorig9:RightHandPinky2": "c_pinky2.r",
    "mixamorig9:RightHandPinky3": "c_pinky3.r",
    "mixamorig9:RightHandPinky4": "c_hand_fk.r",
    "mixamorig9:RightHandRing1": "c_ring1.r",
    "mixamorig9:RightHandRing2": "c_ring2.r",
    "mixamorig9:RightHandRing3": "c_ring3.r",
    "mixamorig9:RightHandRing4": "c_hand_fk.r",
    "mixamorig9:RightHandThumb1": "c_thumb1.r",
    "mixamorig9:RightHandThumb2": "c_thumb2.r",
    "mixamorig9:RightHandThumb3": "c_thumb3.r",
    "mixamorig9:RightHandThumb4": "c_hand_fk.r",
    "mixamorig9:RightLeg": "c_leg_fk.r",
    "mixamorig9:RightShoulder": "c_shoulder.r",
    "mixamorig9:RightToeBase": "c_toes_fk.r",
    "mixamorig9:RightToe_End": "c_toes_fk.r",
    "mixamorig9:RightUpLeg": "c_thigh_fk.r",
    "mixamorig9:Spine": "c_spine_01.x",
    "mixamorig9:Spine1": "c_spine_01.x",
    "mixamorig9:Spine2": "c_spine_02.x",
}

# Get the rigs
source_rig = bpy.data.objects[source_rig_name]
target_rig = bpy.data.objects[target_rig_name]

# Add constraints to target bones
for (
    source_bone_name,
    target_bone_name,
) in bone_map.items():
    try:
        source_bone = source_rig.pose.bones[source_bone_name]
        target_bone = target_rig.pose.bones[target_bone_name]

        # Add Copy Transforms constraint
        constraint = target_bone.constraints.new(type="COPY_TRANSFORMS")
        constraint.target = source_rig
        constraint.subtarget = source_bone_name
    except KeyError:
        print(f"Bone '{source_bone_name}' or '{target_bone_name}' not found.")
        continue

# Bake the animation on the target rig
bpy.ops.object.mode_set(mode="POSE")
bpy.context.view_layer.objects.active = target_rig
bpy.ops.nla.bake(
    frame_start=1,  # Set the start frame
    frame_end=250,  # Set the end frame
    only_selected=False,  # Bake all bones
    visual_keying=True,  # Record the visual result of constraints
    clear_constraints=True,  # Remove constraints after baking
    use_current_action=True,
)

print("Animation retargeting completed.")
