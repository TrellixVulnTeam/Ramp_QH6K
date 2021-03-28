from off_parser import read_off,write_off
from scipy.sparse import lil_matrix ,identity
import numpy as np
import pyvista as pv
import matplotlib.colors 
import sklearn.preprocessing 
blue = np.array([12/256, 238/256, 246/256, 1])

class Mesh(object):
    def __init__(self,path):
        vertices_faces =  read_off(path)
        self.v=vertices_faces[0]
        self.f=vertices_faces[1]
        self.mesh_poly=pv.PolyData(self.v,self.f)
    def vertex_face_adjacency(self):
        adjacency = lil_matrix((len(self.v),len(self.f)))
        for face_index,face in enumerate(self.f):
            for vert_index in face:
                adjacency[vert_index,face_index]=True
        return adjacency > 0
    def vertex_vertex_adjacency(self):
        v_f_adjacency = self.vertex_face_adjacency()
        return (v_f_adjacency*v_f_adjacency.transpose() - identity(len(self.v)))>0
    def vertex_degree(self):
        v_v_adjecency = self.vertex_vertex_adjacency()
        return v_v_adjecency*np.ones(len(self.v))
    def render_wireframe(self):
        pv.plot(pv.PolyData(self.v,self.f),style="wireframe")
    def render_pointcloud(self,color_func):
        plotter=pv.Plotter()
        plotter.add_mesh(self.mesh_poly,cmap="Sequential",style="points",point_size=100,render_points_as_spheres=True,scalars=color_func)
        plotter.show()
        # pv.plot(pv.PolyData(self.v),cmap=np.random.rand(len(self.v)))
    def render_surface(self,color_func,**kwargs):
        plotter=pv.Plotter()
        plotter.add_mesh(self.mesh_poly,cmap=kwargs["cmap"],scalars=np.random.rand(len(self.f)))
        plotter.show()
    def calculate_cross_product(self,face):
        edge1 = self.v[face[1]]-self.v[face[2]]
        edge2 = self.v[face[1]]-self.v[face[3]]
        normal=np.cross(edge1,edge2)
        normal = normal/np.linalg.norm(normal)        
        return normal
    def calculate_face_normals(self):
        normal = np.apply_along_axis(self.calculate_cross_product,axis=1,arr=self.f)
        return normal
        # print(edge1)
    def calculate_face_barycenters(self):
        vertex = np.array(self.v)
        calc = self.vertex_face_adjacency().transpose()*vertex
        return sklearn.preprocessing.normalize(calc,axis=1,norm='l2')        

mesh =Mesh("torus_fat_r2.off")
print(mesh.calculate_face_barycenters())
# mesh.render_surface(vert_deg)