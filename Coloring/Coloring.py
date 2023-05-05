import dip
import math


class Coloring:

    def intensity_slicing(self, image, n_slices):
        '''
       Convert greyscale image to color image using color slicing technique.
       takes as input:
       image: the grayscale input image
       n_slices: number of slices
        
       Steps:
 
        1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        2. Randomly assign a color to each interval
        3. Create and output color image
        4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
 
       returns colored image
       '''
        interval_size = math.ceil((dip.max(image) - dip.min(image)) / (n_slices + 1))

        rows, cols = image.shape
        color_image = dip.zeros(image.shape + (3,), dtype=dip.uint8)
        colors = dip.zeros((n_slices + 1, 3), dtype = dip.uint8)

        for i in range(n_slices + 1):
            red = dip.random.randint(0,255)
            green = dip.random.randint(0,255)
            blue = dip.random.randint(0,255)
            colors[i] = (red,green,blue)

        for i in range(rows):
            for j in range(cols):
                if image[i,j] == 0:
                    continue
                interval = int((image[i,j] - 1) // interval_size)
                color_image[i,j] = colors[interval]

        return color_image

    def color_transformation(self, image, n_slices, theta):
        '''
        Convert greyscale image to color image using color transformation technique.
        takes as input:
        image:  grayscale input image
        colors: color array containing RGB values
        theta: (phase_red, phase,_green, phase_blue) a tuple with phase values for (r, g, b) 
        Steps:
  
         1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
         2. create red values for each slice using 255*sin(slice + theta[0])
            similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
         3. Create and output color image
         4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
  
        returns colored image
        '''

        return image



        

