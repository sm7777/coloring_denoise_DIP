import math
import dip

class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        
        # global_var: noise variance to be used in the Local noise reduction filter        
        self.global_var = var
        
        # S_max: Maximum allowed size of the window that is used in adaptive median filter
        self.S_max = 15

        self.orig_filter_size = filter_size
    

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        return sum(roi)/len(roi)

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        product = 1
        for intensity in roi:
            product = product * intensity

        return product ** (1/ len(roi))
    

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        self.global_var
        local_mean = self.get_arithmetic_mean(roi)
        g_xy = roi[(len(roi) // 2) + 1]
        local_mean = self.get_arithmetic_mean(roi)

        sum = 0
        for num in roi:
            sum = sum + (num - local_mean) ** 2

        local_var = sum / len(roi)

        if self.global_var == 0:
            return g_xy
        else:
            return g_xy - (self.global_var / local_var)*(g_xy - local_mean)


    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        nums = sorted(roi)
        if len(nums) % 2 == 0:
            low_i = len(nums)/2
            high_i = low_i + 1
            median = (nums[low_i] + nums[high_i]) / 2.0
        else:
            index = (len(nums) // 2) + 1
            median = nums[index]
        
        return median
    
    def zero_pad(self):

        if self.filter == self.get_adaptive_median:
            pad = self.S_max // 2
        else:
            pad = self.filter_size // 2

        dimensions = self.image.shape
        width = dimensions[0] + 2 * pad
        height = dimensions[1] + 2 * pad
        zero_padded_image = dip.zeros((width, height))

        for row in range(dimensions[0]):
            for col in range(dimensions[1]):
                zero_padded_image[row + pad][col + pad] = self.image[row][col]

        return zero_padded_image
    
    def get_roi(self, zp_image, xy):

        x = xy[0]
        y = xy[1]

        i_start = -(self.filter_size // 2)
        i_end = i_start + self.filter_size
        j_start = -(self.filter_size // 2)
        j_end = j_start + self.filter_size
        roi = []

        for i in range(i_start, i_end):
            for j in range(j_start, j_end):
                roi.append(zp_image[x + i][y + j])

        return roi
    
    
    def get_adaptive_median(self):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """
        rows, cols = self.image.shape
        new_image = dip.zeros((rows, cols))
        zp_image = self.zero_pad()
        pad = self.S_max // 2

        for i in range(rows):
            self.filter_size = self.orig_filter_size
            for j in range(cols):
                roi = self.get_roi(zp_image, (i + pad, j + pad))

                z_min = 0
                z_max = 0
                z_med = 0
                z_xy = 0

                #Level A
                while(self.filter_size < self.S_max):
                    
                    z_min = min(roi)
                    z_max = max(roi)
                    z_med = self.get_median(roi)
                    z_xy = self.image[i,j]

                    A1 = z_med - z_min
                    A2 = z_med - z_max

                    if A1 > 0 and A2 < 0:
                        break
                    else:
                        self.filter_size += 2
                        roi = self.get_roi(zp_image, (i + pad, j + pad))

                #level B
                B1 = z_xy - z_min
                B2 = z_xy - z_max
                if B1 > 0 and B2 < 0:
                     new_image[i,j] = z_xy
                else:
                    new_image[i,j] = z_med


        return new_image


    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """

        dims = self.image.shape
        new_image = dip.zeros(dims)

        if self.filter == self.get_adaptive_median:
            new_image = self.get_adaptive_median()

        else:

            pad = self.filter_size // 2
            zp_image = self.zero_pad()
            rows, cols = zp_image.shape

            for i in range(pad, rows - pad):
                for j in range(pad, cols - pad):
                    roi = self.get_roi(zp_image, (i,j))
                    new_image[i-pad][j-pad] = self.filter(roi)

                  
        return new_image

