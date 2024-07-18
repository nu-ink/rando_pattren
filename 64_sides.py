from vpython import canvas, vector, color, compound, quad, rate, scene
import math
import numpy as np

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
    compound: A compound object representing the hexecontatetrahedron.
    """
    if radius <= 0:
        raise ValueError("Radius must be positive")

    if not 0 <= face_opacity <= 1:
        raise ValueError("Opacity must be between 0 and 1")

    phi = (1 + math.sqrt(5)) / 2  # Golden ratio

    # Generate vertices using numpy for efficiency
    x = np.array([-1, 1])
    y = np.array([-1, 1])
    z = np.array([-1, 1])

    vertices = []
    for i in x:
        for j in y:
            for k in z:
                vertices.extend([
                    vector(i, j, k),
                    vector(0, i * phi, j / phi),
                    vector(i / phi, 0, j * phi),
                    vector(i * phi, j / phi, 0)
                ])

    # Scale vertices
    vertices = [v.norm() * radius for v in vertices]

    # Create faces
    faces = [vertices[i:i+4] for i in range(0, len(vertices), 4)]

    return compound(
        [
            quad(vs=face, color=face_color, opacity=face_opacity)
            for face in faces
        ]
    )

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
            hexecontatetrahedron.rotate(angle=0, axis=vector(0, 1, 0))
        elif key == 'c':  # Change color
            new_color = color.random()
            hexecontatetrahedron.color = new_color
    
    # Rotate if not paused
    if not pause:
        hexecontatetrahedron.rotate(angle=rotation_speed, axis=vector(0, 1, 0))

print("Animation ended")