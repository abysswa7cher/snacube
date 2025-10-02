from math import sin, cos, radians
from src.classes.mesh import Mesh
from src.classes.helpers.vectors import Vector3


class OBJ:
    """
    Helper class for reading OBJ files and performing direct transformations on the model.
    """
    def __init__(self, path=None):
        self.meshes = list()
        if path is not None:
            with open(path) as file:
                self.read_obj(file)

        self.world_position = Vector3()
        self.world_rotation = Vector3()
        self.world_scale = Vector3(1, 1, 1)

    def read_obj(self, file):
        text = file.read()
        data = [line.split() for line in text.split("\n")[2:] if line != ""]
        vertices = dict()

        i = 1
        j = 1
        for line in data:
            if line[0] == "v":
                v = Vector3.from_list([float(c) for c in line[1:]])
                vertices.update({i: v})
                i += 1

        for mesh_text in [block.split("\n") for block in text.split("o ")][1:]:

            mesh_faces = list()
            mesh_vertices = dict()

            for line in [line.split() for line in mesh_text]:
                if len(line) > 0:
                    if line[0] == "f":
                        verts = [int(v.split("/")[0]) for v in line[1:]]
                        mesh_faces.append(verts)

                        for v in verts:
                            mesh_vertices.update({v: vertices[v]})

            self.meshes.append(Mesh(mesh_vertices, mesh_faces, mesh_text[0]))

    def rotate(self, vector: Vector3):
        self.world_rotation += Vector3(
            round(radians(vector.x), 2),
            round(radians(vector.y), 2),
            round(radians(vector.z), 2),
        )

    def get_transformed_vertex(self, vertex):
        local_vertex = vertex

        scaled_vertex = local_vertex * self.world_scale

        rotated_vertex = scaled_vertex
        if self.world_rotation.x != 0:
            cos_x = cos(self.world_rotation.x)
            sin_x = sin(self.world_rotation.x)
            rotated_vertex = Vector3(
                rotated_vertex.x,
                rotated_vertex.y * cos_x - rotated_vertex.z * sin_x,
                rotated_vertex.y * sin_x + rotated_vertex.z * cos_x,
            )

        if self.world_rotation.y != 0:
            cos_y = cos(self.world_rotation.y)
            sin_y = sin(self.world_rotation.y)
            rotated_vertex = Vector3(
                rotated_vertex.x * cos_y + rotated_vertex.z * sin_y,
                rotated_vertex.y,
                -rotated_vertex.x * sin_y + rotated_vertex.z * cos_y,
            )

        if self.world_rotation.z != 0:
            cos_z = cos(self.world_rotation.z)
            sin_z = sin(self.world_rotation.z)
            rotated_vertex = Vector3(
                rotated_vertex.x * cos_z - rotated_vertex.y * sin_z,
                rotated_vertex.x * sin_z + rotated_vertex.y * cos_z,
                rotated_vertex.z,
            )

        transformed_vertex = Vector3(
            rotated_vertex.x + self.world_position.x,
            rotated_vertex.y + self.world_position.y,
            rotated_vertex.z + self.world_position.z,
        )

        return transformed_vertex
