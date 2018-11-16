import bpy
import os
import sys
k= str(sys.argv[5])
def import_export(k):
    file_loc = 'static\\JS\\3DModels\\'+k
    imported_object = bpy.ops.import_mesh.stl(filepath=file_loc, axis_forward='-Z', axis_up='Y')
    object1=imported_object
    obj_object = bpy.context.selected_objects[0]
    path = bpy.path.abspath('static\\JS\\3DModels\\')
    if not os.path.exists(path):
        os.makedirs(path)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[obj_object.name].select = True
    fPath = str((path + obj_object.name + '.obj'))
    bpy.ops.export_scene.obj(filepath=fPath, axis_forward='-Z', axis_up='Y')


def centroid():
    sum1=0
    count1=0
    sum2=0
    sum3=0
    obj_data = bpy.data.objects[obj].data
    for v in obj_data.vertices:
        sum1=sum1+v.co[0]
        count1=count1+1
        sum2=sum2+v.co[1]
        sum3=sum3+v.co[2]
    sum1=sum1/count1;
    sum2=sum2/count1;
    sum3=sum3/count1;
    fin=[]
    fin.append(sum1)
    fin.append(sum2)
    fin.append(sum3)
    os.system("cd static\\JS\\3DModels && blender.py "+fin)
    print(str(sum1/count1)+" "+str(sum2/count1)+" "+str(sum3/count1))
import_export(k)
centroid();
bpy.ops.object.delete()
