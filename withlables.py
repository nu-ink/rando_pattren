import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def create_custom_colormap():
    """Create a custom colormap for the flower of life."""
    colors = ['#FFA07A', '#98FB98', '#87CEFA', '#DDA0DD', '#F0E68C']
    return LinearSegmentedColormap.from_list("custom", colors, N=100)

def draw_flower_of_life(ax, center, radius, depth, colormap):
    if depth == 0:
        return
    
    # Draw the central circle with a color based on depth
    color = colormap(1 - depth / 4)  # Adjust color based on depth
    circle = plt.Circle(center, radius, edgecolor='black', facecolor=color, alpha=0.6)
    ax.add_artist(circle)
    
    # Calculate the positions of the 6 surrounding circles
    for angle in np.linspace(0, 2*np.pi, 7)[:-1]:
        new_center = (center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle))
        draw_flower_of_life(ax, new_center, radius, depth - 1, colormap)

def draw_mandala(ax, center, radius):
    """Draw a mandala in the background."""
    n_points = 12
    angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    for i in range(5):
        x = center[0] + (radius * (i+1)/5) * np.cos(angles)
        y = center[1] + (radius * (i+1)/5) * np.sin(angles)
        ax.plot(x, y, 'k-', alpha=0.2, linewidth=0.5)
    
    for angle in angles:
        ax.plot([center[0], center[0] + radius * np.cos(angle)],
                [center[1], center[1] + radius * np.sin(angle)],
                'k-', alpha=0.2, linewidth=0.5)

def main():
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    # Create custom colormap
    colormap = create_custom_colormap()
    
    # Define the initial parameters
    initial_center = (0, 0)
    initial_radius = 1
    depth = 4  # The depth of recursion to create a more complex pattern
    
    # Draw background mandala
    draw_mandala(ax, initial_center, 5)
    
    # Draw the Flower of Life
    draw_flower_of_life(ax, initial_center, initial_radius, depth, colormap)
    
    # Set the limits to make sure the pattern fits in the plot
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    
    # Add title
    plt.title("Enhanced Flower of Life", fontsize=20, pad=20)
    
    # Add subtle grid
    ax.grid(color='gray', linestyle=':', linewidth=0.5, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()