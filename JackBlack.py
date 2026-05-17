import numpy as np 
import matplotlib.pyplot as plt

#480 * 270 pixels til visualisering og udregninger.
width = 350
height = 350

#simpelt sort hul. Pixels bliver mørke når de er tæt på midten
Event_horizon = 160.0

#Position af sort hul og "kamera"
kamera_pos = np.array([0.0, 0.0, -500.0])
black_hole_pos = np.array([0.0, 0.0, 0.0])

def generate_starry_background(width, height):
    background = np.zeros((height, width, 3))
    star_density = 0.025  #2.5% af pixels er stjerner
    num_stars = int(width * height * star_density)
    
    star_y = np.random.randint(0, height, num_stars)
    star_x = np.random.randint(0, width, num_stars)
    background[star_y, star_x] = [1.0, 1.0, 1.0] 
    
    return background

def trace_ray(x, y):
    #Normalt koordinat system (0,0) oppe til venstre og stiger mod højre mens y falder når den går ned
    px = (x / width) * 2 - 1
    py = (y / height) * 2 - 1
    
    #Lysstråle retning
    ray_dir = np.array([px, py, 1.0])
    ray_dir /= np.linalg.norm(ray_dir)
    
    #Udregn minimum afstand fra lysstråle til midte af sort hul 
    #Using the formula for distance from point to line
    ray_origin = kamera_pos
    cross = np.cross(ray_dir, black_hole_pos - ray_origin)
    min_distance = np.linalg.norm(cross) / np.linalg.norm(ray_dir)
    
    #Checker om pixel er inden for radius af sort hul
    if min_distance < Event_horizon:
        return np.array([0.0, 0.0, 0.0])  
    else:
        return None  
def render():
    image = generate_starry_background(width, height)
    
    #Trace rays for each pixel
    for y in range(height):
        for x in range(width):
            color = trace_ray(x, y)
            if color is not None:
                image[y, x] = color
    
    # Load accretion disk on top of everything
    disk = accretion_disk(width, height)
    image = np.maximum(image, disk)
    
    return image

def accretion_disk(width, height):
    disk = np.zeros((height, width, 3))
    disk[175,175] = [1.0, 1.0, 0.0]  # Yellow pixel
    return disk
#da black hole
#Vi vil sætte det sorte hul ved koordinaterne (0,0,0) og kameraet ved (0,0,-500) så vi kigger på det sorte hul

if __name__ == "__main__":
    print("Showing da black man...")
    image = render()
    
    plt.figure(figsize=(12, 7))
    plt.imshow(image)
    plt.title("Black Hole Visualization")
    plt.axis('off')
    plt.tight_layout()
    plt.show()