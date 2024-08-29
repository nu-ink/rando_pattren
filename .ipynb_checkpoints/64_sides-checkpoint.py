from vpython import canvas, vector, color, triangle, rate, scene
import math
import random
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
    list: A list of triangle objects representing the hexecontatetrahedron.
    """
    if radius <= 0:
        raise ValueError("Radius must be positive")
    
    if not 0 <= face_opacity <= 1:
        raise ValueError("Opacity must be between 0 and 1")

    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    
    # Use numpy for efficient vertex generation
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

# Global dictionary to keep track of key states
key_states = {}

def keydown(evt):
    """Handler for keydown events"""
    key_states[evt.key] = True

def keyup(evt):
    """Handler for keyup events"""
    key_states[evt.key] = False

# Bind the keydown and keyup handlers to the scene
scene.bind('keydown', keydown)
scene.bind('keyup', keyup)

def keysdown():
    """Returns a list of currently pressed keys"""
    return [key for key, pressed in key_states.items() if pressed]

# Animation settings
rotation_speed = 0.02
pause = False
recent_key_press = {key: False for key in ['p', 'c', 'r']}

# Animation loop
try:
    while True:
        rate(30)  # 30 frames per second
        
        # Handle keyboard input
        keys = keysdown()
        
        if 'q' in keys:  # Quit
            break
        elif 'p' in keys and not recent_key_press['p']:  # Pause/Resume
            pause = not pause
            recent_key_press['p'] = True
            scene.sleep(0.2)  # 200ms delay
        elif 'r' in keys and not recent_key_press['r']:  # Reset rotation
            for face in hexecontatetrahedron:
                face.rotate(angle=-face.orientation.angle, axis=face.orientation.axis)
            recent_key_press['r'] = True
            scene.sleep(0.2)  # 200ms delay
        elif 'c' in keys and not recent_key_press['c']:  # Change color
            new_color = vector(random.random(), random.random(), random.random())
            for face in hexecontatetrahedron:
                face.color = new_color
            recent_key_press['c'] = True
            scene.sleep(0.2)  # 200ms delay
        elif 'up' in keys:  # Increase rotation speed
            rotation_speed *= 1.1
        elif 'down' in keys:  # Decrease rotation speed
            rotation_speed /= 1.1
        
        # Reset recent key press flags
        for key in recent_key_press:
            if key not in keys:
                recent_key_press[key] = False
        
        # Rotate if not paused
        if not pause:
            for face in hexecontatetrahedron:
                face.rotate(angle=rotation_speed, axis=vector(0, 1, 0))

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Animation ended")
    print(f"Final rotation speed: {rotation_speed:.4f}")