from PIL import ImageDraw

from src.classes.render_turtle import RenderTurtle
from src.classes.helpers.obj import OBJ
from src.classes.helpers.vectors import Vector2
from src.globals import SCREEN_WIDTH, SCREEN_HEIGHT, TRACER_COLOR


class Model(OBJ):
    """
    Model class, wrapper for an OBJ file object, since OBJ models can contain several meshes.
    """
    def __init__(self, turtle: RenderTurtle, path=None):
        super().__init__(path)
        self.turtle = turtle

    def __repr__(self):
        return f"Model(pos: {self.world_position}, rot: {self.world_rotation}, scale: {self.world_scale})"

    def draw(self, camera):
        transformed_verts = []

        for mesh in self.meshes:
            t_mesh_verts = dict()
            color = mesh.color
            for key, vertex in mesh.verts.items():
                transformed = self.get_transformed_vertex(vertex)
                screen_point = camera.project_point(transformed)
                t_mesh_verts.update(
                    {key: Vector2(int(screen_point.x), int(screen_point.y))}
                )
            transformed_verts.append([t_mesh_verts, color])

        for i, mesh in enumerate(self.meshes):
            color = transformed_verts[i][1]
            self.turtle.pencolor(color)
            for edges in mesh.edges:
                
                for edge in edges:
                    v1 = [
                        transformed_verts[i][0][edge[0]].x,
                        transformed_verts[i][0][edge[0]].y,
                    ]
                    v2 = [
                        transformed_verts[i][0][edge[1]].x,
                        transformed_verts[i][0][edge[1]].y,
                    ]
                    
                    self.turtle.teleport(
                        -SCREEN_WIDTH // 2 + v1[0], -SCREEN_HEIGHT // 2 + v1[1]
                    )
                    self.turtle.goto(
                        -SCREEN_WIDTH // 2 + v2[0], -SCREEN_HEIGHT // 2 + v2[1]
                    )
        self.turtle.pencolor(TRACER_COLOR)