import bpy
import numpy as np
import mathutils

def best_fit_transform(A, B):
    '''
    Calculates the least-squares best-fit transform that maps corresponding points A to B in m spatial dimensions
    Input:
      A: Nxm numpy array of corresponding points
      B: Nxm numpy array of corresponding points
    Returns:
      T: (m+1)x(m+1) homogeneous transformation matrix that maps A on to B
      R: mxm rotation matrix
      t: mx1 translation vector
    '''

    assert A.shape == B.shape

    # get number of dimensions
    m = A.shape[1]

    # translate points to their centroids
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    AA = A - centroid_A
    BB = B - centroid_B

    # rotation matrix
    H = np.dot(AA.T, BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
       Vt[m-1,:] *= -1
       R = np.dot(Vt.T, U.T)

    # translation
    t = centroid_B.T - np.dot(R,centroid_A.T)

    # homogeneous transformation
    T = np.identity(m+1)
    T[:m, :m] = R
    T[:m, m] = t
    return T, R, t


def nearest_neighbor(src, dst):
    '''
    Find the nearest (Euclidean) neighbor in dst for each point in src
    Input:
        src: Nxm array of points
        dst: Nxm array of points
    Output:
        distances: Euclidean distances of the nearest neighbor
        indices: dst indices of the nearest neighbor
    '''

    assert src.shape == dst.shape

    distances = []
    indices = []

    for point_src in src:
        min_distance = float('inf')
        print("just for testing")
        nearest_index = Nonne
        for i, point_dst in enumerate(dst):
            distance = np.linalg.norm(point_src - point_dst)
            if distance < min_distance:
                min_distance = distance
                nearest_index = i
        distances.append(min_distance)
        indices.append(nearest_index)
        
    print(indices)
    return np.array(distances), np.array(indices)


def icp(A, B, init_pose=None, max_iterations=100, tolerance=0.000):
    '''
    The Iterative Closest Point method: finds best-fit transform that maps points A on to points B
    Input:
        A: Nxm numpy array of source mD points
        B: Nxm numpy array of destination mD point
        init_pose: (m+1)x(m+1) homogeneous transformation
        max_iterations: exit algorithm after max_iterations
        tolerance: convergence criteria
    Output:
        T: final homogeneous transformation that maps A on to B
        distances: Euclidean distances (errors) of the nearest neighbor
        i: number of iterations to converge
    '''

    assert A.shape == B.shape

    # get number of dimensions
    m = A.shape[1]

    # make points homogeneous, copy them to maintain the originals
    src = np.ones((m+1,A.shape[0]))
    dst = np.ones((m+1,B.shape[0]))
    src[:m,:] = np.copy(A.T)
    dst[:m,:] = np.copy(B.T)

    # apply the initial pose estimation
    if init_pose is not None:
        src = np.dot(init_pose, src)

    prev_error = 0

    for i in range(max_iterations):
        # find the nearest neighbors between the current source and destination points
        distances, indices = nearest_neighbor(src[:m,:].T, dst[:m,:].T)

        # compute the transformation between the current source and nearest destination points
        T,_,_ = best_fit_transform(src[:m,:].T, dst[:m,indices].T)

        # update the current source
        src = np.dot(T, src)

        # check error
        mean_error = np.mean(distances)
        if np.abs(prev_error - mean_error) < tolerance:
            break
        prev_error = mean_error

    # calculate final transformation
    T,R,_ = best_fit_transform(A, src[:m,:].T)
    #print(R)
    return T, distances, i


class CustomOperator(bpy.types.Operator):
    bl_idname = "object.custom_operator"
    bl_label = "Custom Operator"

    def execute(self, context):
        #Specify your object here
        obj = bpy.data.objects.get("Cube")
        obj2 = bpy.data.objects.get("Cube.001")

        if obj is not None:
            vertices = [obj.matrix_world @ v.co for v in obj.data.vertices]
            PC1 = np.array([vertex for vertex in vertices])
            print(PC1[0])
        else:
            print("object does not exist")
            
        if obj2 is not None:
            vertices = [obj2.matrix_world @ v.co for v in obj2.data.vertices]
            PC2 = np.array([vertex for vertex in vertices])
            print(PC2[0])
        else:
            print("object does not exist")
            
            
        T,_,_ = icp(PC1, PC2)
        np.set_printoptions(suppress=True)
        print(T)
        rotation_matrix = mathutils.Matrix(T.tolist())
        obj.matrix_world = rotation_matrix
        obj.scale = obj2.scale
        bpy.context.view_layer.update()
        print("Button clicked. Running script...")
        return {'FINISHED'}


#UI
class CustomPanel(bpy.types.Panel):
    bl_label = "Custom Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Custom'

    def draw(self, context):
        layout = self.layout

        # Add a button to run the operator
        layout.operator("object.custom_operator", text="Run Script")

def register():
    bpy.utils.register_class(CustomOperator)
    bpy.utils.register_class(CustomPanel)

def unregister():
    bpy.utils.unregister_class(CustomOperator)
    bpy.utils.unregister_class(CustomPanel)

if __name__ == "__main__":
    register()




