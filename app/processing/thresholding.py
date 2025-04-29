import numpy as np


class Thresholding:
    @staticmethod
    def spectral_thresholding(image):
        # Step 1: Build histogram 
        hist, _ = np.histogram(image, bins=256, range=(0, 256))

        # Step 2: Smooth histogram  (simple moving average)
        window_size = 5
        hist_smooth = np.convolve(hist, np.ones(window_size) / window_size, mode='same')

        # Step 3: Find peaks 
        peaks = []
        for i in range(1, len(hist_smooth) - 1):
            if hist_smooth[i] > hist_smooth[i - 1] and hist_smooth[i] > hist_smooth[i + 1]:
                peaks.append(i)

        # Step 4: Safety check
        if len(peaks) < 2:
            mean_value = np.mean(image)
            segmented = np.where(image > mean_value, 255, 0).astype(np.uint8)
            return segmented

        # Step 5: Set thresholds
        thresholds = []
        for i in range(len(peaks) - 1):
            midpoint = (peaks[i] + peaks[i + 1]) // 2
            thresholds.append(midpoint)

        # Step 6: Apply thresholding 
        segmented = np.zeros_like(image)

        if len(thresholds) == 1:
            t1 = thresholds[0]
            segmented[image <= t1] = 0
            segmented[image > t1] = 255

        elif len(thresholds) == 2:
            t1, t2 = thresholds
            segmented[image <= t1] = 0
            segmented[(image > t1) & (image <= t2)] = 127
            segmented[image > t2] = 255

        else:
            values = np.linspace(0, 255, len(thresholds) + 1, dtype=np.uint8)
            prev_thresh = 0
            for i, t in enumerate(thresholds):
                segmented[(image > prev_thresh) & (image <= t)] = values[i]
                prev_thresh = t
            segmented[image > thresholds[-1]] = values[-1]

        return segmented

    @staticmethod
    def optimal_thresholding(block):
        # get image dimensions and initialize output
        height, width = block.shape
        output_block = block.copy()

        # create object and background masks to divide pixels into 2 arrays
        bg_mask = np.zeros_like(block, dtype=bool)
        bg_mask[0, 0] = True
        bg_mask[height - 1, 0] = True
        bg_mask[0, width - 1] = True
        bg_mask[height - 1, width - 1] = True
        obj_mask = ~bg_mask

        # parameter to keep track of iterations
        new_threshold=0
   
        for i in range(20):

            # update the thresholds
            previous_threshold=new_threshold

            # use the masks to extract object and background pixels
            obj_pixels = output_block[obj_mask]
            bg_pixels = output_block[bg_mask]

            # find mean of bg and obj pixel values
            obj_mean = np.mean(obj_pixels)
            bg_mean = np.mean(bg_pixels)

            # compute threshold (T) as their avg bg+obj/2  (avg of means)
            new_threshold = (obj_mean + bg_mean) / 2

            # redefine the masks to separate object and background pixels using new threshold
            obj_mask = output_block > new_threshold
            bg_mask = output_block <= new_threshold

            # if threshold value stops changing, end the loop
            if (np.abs(previous_threshold-new_threshold)<2):
                break

        # finally threshold the image using the optimally computed threshold
        output_block[block >= new_threshold] = 255  
        output_block[block < new_threshold] = 0   

        return output_block

    def otsu_thresholding(block):
        # initalize variance array and output block
        variances = np.zeros(256)
        output_block = block.copy()

        # GET histogram, indexed from 0-->255 and values are the frequencies
        histogram, bin_edges = np.histogram(output_block, bins=256, range=(0, 256))
        total_pixels = np.sum(histogram)  

        # Loop over all intensity values (0-->255), each time dividing the histograms into 2 classes at intensity i 
        for i in range (0,256):

            # compute weights of the 2 classes:
            obj_weight = np.sum(histogram[i:256]) / total_pixels
            bg_weight = np.sum(histogram[0:i]) / total_pixels
           
            # compute mean of the 2 classes:
            obj_intensities = np.sum(histogram[i:256])
            bg_intensities = np.sum(histogram[0:i])

            # ensure no division by zero
            if obj_intensities != 0:
                obj_mean = np.sum(np.arange(i, 256) * histogram[i:256]) / obj_intensities
            else:
                obj_mean = 0

            if bg_intensities != 0:
                bg_mean = np.sum(np.arange(0, i) * histogram[0:i]) / bg_intensities
            else:
                bg_mean = 0

            # compute variance using the weights and means
            variances[i]=obj_weight*bg_weight*((obj_mean-bg_mean)**2)

        # Find the index of the maximun variance, this is my intensity threshold value 
        otsu_threshold=np.argmax(variances)

        # threshold the image based on the otsu threshold computed
        output_block[block>=otsu_threshold]=255
        output_block[block<otsu_threshold]=0

        return output_block


    @staticmethod
    def local_thresholding(image, thresholding_method, block_size=30):
        # initialize output image and get dimensions
        height, width = image.shape
        output_image = np.zeros_like(image, dtype=np.int8)

        for i in range(0, height, block_size):
            for j in range(0, width, block_size):
                # this loop extracts windows with size block_sizexblock_size
                window = image[i:min(i + block_size, height), j:min(j + block_size, width)]
                # window selected is passed to the chosen thresholding method and a thresholded window is return
                thresholded_window = thresholding_method(window)
                # reconstruct the entire image window by window
                output_image[i:min(i + block_size, height), j:min(j + block_size, width)] = thresholded_window

        return output_image
    
