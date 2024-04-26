import bpy
from math import radians
import math
import os
from mathutils import Vector
import bmesh

class FLS:
    def __init__(self, frame, index, color, position):
        self.frame = frame
        self.index = index
        self.color = color
        self.position = position
'''
# Select the object you want to animate
bpy.data.objects["Sphere"].select_set(True)
#print(bpy.data.objects["Cylinder"].select_get())

for obj in bpy.data.objects:
    if obj.animation_data is not None:
        obj.animation_data_clear()


# Set the initial rotation
obj.rotation_euler = (radians(0), radians(0), radians(0))
obj.location = (0, 0, 0)
obj.scale = (10, 10, 10)
# Set the number of frames for the animation
num_frames = 33

# Keyframe the rotation at frame 1
obj.keyframe_insert(data_path="scale", frame=1)
obj.keyframe_insert(data_path="location", frame=1)
obj.keyframe_insert(data_path="rotation_euler", frame=1)

# Set the final rotation
obj.rotation_euler = (radians(0), radians(0), radians(360))
obj.location = (100, 0, 0)
obj.scale = (50, 50, 50)

# Keyframe the rotation at the last frame
obj.keyframe_insert(data_path="scale", frame=num_frames)
obj.keyframe_insert(data_path="location", frame=num_frames)
obj.keyframe_insert(data_path="rotation_euler", frame=num_frames)

# Set the scene frame range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = num_frames

anim_data = obj.animation_data
if anim_data is not None:
    for fcurve in anim_data.action.fcurves:
        fcurve.extrapolation = 'LINEAR'
'''

# 获取场景中的所有对象
bpy.data.objects["Mix"].select_set(True)

'''
verts = [(100, 0, 100)]  # 2 verts made with XYZ coords
mesh = bpy.context.object.data
bm = bmesh.new()

# convert the current mesh to a bmesh (must be in edit mode)
bpy.ops.object.mode_set(mode='EDIT')
bm.from_mesh(mesh)
bpy.ops.object.mode_set(mode='OBJECT')  # return to object mode

for v in verts:
    bm.verts.new(v)  # add a new vert

# make the bmesh the object's mesh
bm.to_mesh(mesh)  
bm.free()  # always do this when finished
'''
for obj in bpy.data.objects:
    if obj.animation_data is not None:
        obj.animation_data_clear()
        
print(obj.data.vertices[42].co)


#print(bpy.data.curves["NurbsPath.002"].name)
obj.keyframe_insert(data_path='constraints["Follow Path"].offset', frame=1)
obj.rotation_euler = (radians(0), radians(0), radians(0))
obj.keyframe_insert(data_path="rotation_euler", frame=1)

obj.keyframe_insert(data_path='constraints["Follow Path"].offset', frame=33)
obj.rotation_euler = (radians(0), radians(0), radians(360))
obj.keyframe_insert(data_path="rotation_euler", frame=33)

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 33

anim_data = obj.animation_data
if anim_data is not None:
    for fcurve in anim_data.action.fcurves:
        fcurve.extrapolation = 'LINEAR'
                    

Xwm_matrices = []
Xwm_rotation_matrices = []
Xwm_rotation_euler = []
Vertex_Positions = []
if anim_data is not None and anim_data.action is not None:
    start_frame = int(anim_data.action.frame_range[0])
    end_frame = int(anim_data.action.frame_range[1])
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        Xwm_matrices.append(obj.matrix_world.copy())
        Xwm_rotation_matrices.append(obj.rotation_euler.to_matrix().to_4x4().copy())
        Xwm_rotation_euler.append(obj.rotation_euler.copy())
        Vertex_Positions.append(obj.data.copy())

FLS_data_per_frame = []
if anim_data is not None and anim_data.action is not None:
    start_frame = int(anim_data.action.frame_range[0])
    end_frame = int(anim_data.action.frame_range[1])
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        fls_objects = []
        for vertex in obj.data.vertices:
            vertex_coordinates_world = Xwm_rotation_matrices[frame-1] @ vertex.co
            fls_obj = FLS(frame=frame, index=vertex.index, color=(0, 1, 0), position=vertex_coordinates_world)
            fls_objects.append(fls_obj)
            
        FLS_data_per_frame.append(fls_objects)


def Round(coordinate):
    precision = 3
    coordinate = Vector((round(coordinate[0], precision), 
    round(coordinate[1], precision), round(coordinate[2], precision))) 
    
    return coordinate

vertices_to_change_indexes = []   
vertices_to_change_indexes_lists = []
def check_cycle(obj, frame, hashed_points, vertex_index, cycle_start_index):
    bpy.context.scene.frame_set(frame)
    vertex_coordinates_world = Round(FLS_data_per_frame[frame-1][vertex_index].position)
    vertex_coordinates_world.freeze()
    if vertex_coordinates_world in hashed_points:
        vertices_to_change_indexes.append(vertex_index)
        if hashed_points[vertex_coordinates_world] == cycle_start_index:
            return True
        else:
            return check_cycle(obj, frame, hashed_points, hashed_points[vertex_coordinates_world], cycle_start_index)
    else:
        return False  
  
def Deploy_Dark_FLSs(Xwm_rotation_matrix, obj, dark_FLS_coordinate, starting_point):
    tmp_co = Round(obj.data.vertices[starting_point].co)
    if dark_FLS_coordinate == tmp_co:
        return True
    else:
        if dark_FLS_coordinate not in hashed_points_model_space:
            verts = dark_FLS_coordinate  # 2 verts made with XYZ coords
            mesh = bpy.context.object.data
            bm = bmesh.new()
            # convert the current mesh to a bmesh (must be in edit mode)
            bpy.ops.object.mode_set(mode='EDIT')
            bm.from_mesh(mesh)
            bpy.ops.object.mode_set(mode='OBJECT')  # return to object mode
            bm.verts.new(verts)  # add a new vert
            # make the bmesh the object's mesh
            bm.to_mesh(mesh)  
            bm.free()  # always do this when finished
            
        dark_FLS_coordinate = Xwm_rotation_matrix @ dark_FLS_coordinate
        dark_FLS_coordinate = Round(dark_FLS_coordinate)
        Deploy_Dark_FLSs(Xwm_rotation_matrix, obj, dark_FLS_coordinate, starting_point)
    
anim_data = obj.animation_data
hashed_points = {}
FLS_Flight_Path_per_frame = []
if anim_data is not None and anim_data.action is not None:
    start_frame = int(anim_data.action.frame_range[0])
    end_frame = int(anim_data.action.frame_range[1])
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        if frame > 1:
            for i in range(0, len(FLS_data_per_frame[frame-1])):
                if any(FLS_data_per_frame[frame-1][i].index in sublist for sublist in vertices_to_change_indexes_lists) == False:
                    vertex_coordinates_world = Round(FLS_data_per_frame[frame-1][i].position)
                    vertex_coordinates_world.freeze()
                    if vertex_coordinates_world in hashed_points:   
                        vertices_to_change_indexes.append(FLS_data_per_frame[frame-1][i].index)
                        if check_cycle(obj, frame, hashed_points, hashed_points[vertex_coordinates_world], FLS_data_per_frame[frame-1][i].index) == True:
                            if len(vertices_to_change_indexes) == 2:
                                if vertices_to_change_indexes[0] == vertices_to_change_indexes[1]:
                                    vertices_to_change_indexes = []
                                else:
                                    vertices_to_change_indexes_lists.append(vertices_to_change_indexes) 
                            else:
                                vertices_to_change_indexes_lists.append(vertices_to_change_indexes) 
                                             
                            vertices_to_change_indexes = []
                        else:
                            #dark_FLS_coordinate = Xwm_rotation_matrices[frame-1] @ obj.data.vertices[i].co
                            #dark_FLS_coordinate = Round(dark_FLS_coordinate)
                            #Deploy_Dark_FLSs(Xwm_rotation_matrices[frame-1], obj, dark_FLS_coordinate, obj.data.vertices[i].index)
                            vertices_to_change_indexes = []
                            
            print("frame ", frame)
            for row in vertices_to_change_indexes_lists:
                print(row)
            '''
            if len(vertices_to_change_indexes_lists) > 0:
                print("Changed Flight Path: ")
                #print(vertices_to_change_indexes_lists)
                for i in range(0, len(vertices_to_change_indexes_lists)):
                    for j in range(0, len(vertices_to_change_indexes_lists[i])):
                        if j-1 >= 0:
                            print(vertices_to_change_indexes_lists[i][j], " -> ", vertices_to_change_indexes_lists[i][j-1])
                            FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][j]].position = FLS_data_per_frame[frame-1-1][vertices_to_change_indexes_lists[i][j]].position
                            #FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][j]].index = vertices_to_change_indexes_lists[i][j-1]
                            FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][j]].color = FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][j-1]].color
                        else:
                            print(vertices_to_change_indexes_lists[i][j], " -> ", vertices_to_change_indexes_lists[i][len(vertices_to_change_indexes_lists[i])-1])
                            FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][j]].position = FLS_data_per_frame[frame-1-1][vertices_to_change_indexes_lists[i][j]].position
                            #FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][j]].index = vertices_to_change_indexes_lists[i][len(vertices_to_change_indexes_lists[i])-1]
                            FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][j]].color = FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][len(vertices_to_change_indexes_lists[i])-1]].color
                        
                        #print(FLS_data_per_frame[frame-1][vertices_to_change_indexes_lists[i][j]].index)    
            '''
        
            
        vertices_to_change_indexes_lists = []  
        hashed_points = {}
        hashed_points_model_space = {}
        for i in range(0, len(FLS_data_per_frame[frame-1])):
            vertex_coordinates_world  = Round(FLS_data_per_frame[frame-1][i].position)
            vertex_coordinates_world.freeze()
            hashed_points[vertex_coordinates_world] = FLS_data_per_frame[frame-1][i].index
            
        for i in range(0, len(obj.data.vertices)):   
            vertex_coordinates_model = Round(obj.data.vertices[i].co)
            vertex_coordinates_model.freeze()
            hashed_points_model_space[vertex_coordinates_model] = obj.data.vertices[i].index