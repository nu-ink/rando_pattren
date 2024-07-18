from vpython import canvas, vector, color, triangle, rate, scene
import math
import random

# Set up the scene
scene = canvas(title='Rotating Hexecontatetrahedron', width=800, height=600, center=vector(0, 0, 0), background=color.white)

def create_hexecontatetrahedron(radius=1, face_color=color.blue, face_opacity=0.7):
    """
    Create a hexecontatetrahedron with a given radius, face color, and opacity.
    
    Parameters:
    radius (float): The radius to scale the vertices of the hexecontatetrahedron.
    face_color (color): The color of the faces.
    face_opacity (float): The opacity of the faces (0 to 1).
    
    Returns:
    list: A list of triangle objects representing the hexecontatetrahedron.
    """
    if radius <= 0:
        raise ValueError("Radius must be positive")
    
    if not 0 <= face_opacity <= 1:
        raise ValueError("Opacity must be between 0 and 1")

    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    
    vertices = []
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                vertices.extend([
                    vector(x, y, z),
                    vector(0, x * phi, y / phi),
                    vector(x / phi, 0, y * phi),
                    vector(x * phi, y / phi, 0)
                ])

    # Scale vertices
    vertices = [v.norm() * radius for v in vertices]
    
    # Create faces
    faces = []
    for i in range(0, len(vertices), 4):
        v = vertices[i:i+4]
        faces.extend([
            triangle(vs=[v[0], v[1], v[2]], color=face_color, opacity=face_opacity),
            triangle(vs=[v[0], v[2], v[3]], color=face_color, opacity=face_opacity),
            triangle(vs=[v[0], v[3], v[1]], color=face_color, opacity=face_opacity),
            triangle(vs=[v[1], v[3], v[2]], color=face_color, opacity=face_opacity)
        ])
    
    return faces

# Create the hexecontatetrahedron
hexecontatetrahedron = create_hexecontatetrahedron(2, color.blue, 0.7)

# Animation settings
rotation_speed = 0.02
pause = False

# Animation loop
while True:
    rate(30)  # 30 frames per second
    
    # Handle keyboard input
    if scene.kb.keys:
        key = scene.kb.getkey()
        if key == 'q':  # Quit
            break
        elif key == 'p':  # Pause/Resume
            pause = not pause
        elif key == 'r':  # Reset rotation
            for face in hexecontatetrahedron:
                face.rotate(angle=-face.orientation.angle, axis=face.orientation.axis)
        elif key == 'c':  # Change color
            new_color = vector(random.random(), random.random(), random.random())
            for face in hexecontatetrahedron:
                face.color = new_color
    
    # Rotate if not paused
    if not pause:
        for face in hexecontatetrahedron:
            face.rotate(angle=rotation_speed, axis=vector(0, 1, 0))

print("Animation ended")