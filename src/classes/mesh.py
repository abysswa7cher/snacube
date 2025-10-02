from random import choice

COLORS = None

try:
    with open("assets/colors.txt") as file:
        COLORS = [line.strip() for line in file.readlines()]
except:
    print("Couldn't load colors.txt file in /assets/ folder")

class Mesh:
    """
    Wrapper class containing vertex data of a single mesh.
    """
    def __init__(self, verts: dict = dict(), faces: list = list(), color: str = str()):
        self.verts = verts
        self.faces = faces
        self.edges = list()
        if COLORS:
            if color in COLORS:
                self.color = color
            else:
                self.color = choice(COLORS)

        self.check_validity()
        self.generate_sides()

        self.verts = dict(
            sorted(self.verts.items(), key=lambda x: x[1].z, reverse=True)
        )

    def generate_sides(self):
        pairs_q = [(0, 1), (1, 2), (2, 3), (3, 0)]
        pairs_t = [(0, 1), (1, 2), (2, 0)]

        for face in self.faces:
            if len(face) == 4:
                self.edges.append([(face[p[0]], face[p[1]]) for p in pairs_q])
            elif len(face) == 3:
                self.edges.append([(face[p[0]], face[p[1]]) for p in pairs_t])
            else:
                raise ValueError(
                    f"Face {face} is not a triangle nor a quad (Vertex count < 3 or > 4)."
                )

    def check_validity(self):
        for face in self.faces:
            for vertex in face:
                if vertex not in self.verts.keys():
                    raise ValueError(
                        "Vertex {} not found in {}".format(vertex, self.verts)
                    )

    def __str__(self):
        return f"\n------\nMesh(\n    Color: {self.color}\n    Vertices: {self.verts}\n    Faces: {self.faces}    \n    Edges: {self.edges}\n)"

    def __repr__(self):
        return f"\n------\nMesh(\n    Color: {self.color}\n    Vertices: {self.verts}\n    Faces: {self.faces}    \n    Edges: {self.edges}\n)"
