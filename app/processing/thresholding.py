import numpy as np


class Thresholding:
    @staticmethod
    def spectral_thresholding(image):
        # Step 1: Convert to grayscale 
        if len(image.shape) == 3:
            gray_image = (0.2989 * image[:, :, 2] + 0.5870 * image[:, :, 1] + 0.1140 * image[:, :, 0]).astype(np.uint8)
        else:
            gray_image = image.copy()

        # Step 2: Build histogram 
        hist, _ = np.histogram(gray_image, bins=256, range=(0, 256))

        # Step 3: Smooth histogram  (simple moving average)
        window_size = 5
        hist_smooth = np.convolve(hist, np.ones(window_size) / window_size, mode='same')

        # Step 4: Find peaks 
        peaks = []
        for i in range(1, len(hist_smooth) - 1):
            if hist_smooth[i] > hist_smooth[i - 1] and hist_smooth[i] > hist_smooth[i + 1]:
                peaks.append(i)

        # Step 5: Safety check
        if len(peaks) < 2:
            mean_value = np.mean(gray_image)
            segmented = np.where(gray_image > mean_value, 255, 0).astype(np.uint8)
            return segmented

        # Step 6: Set thresholds
        thresholds = []
        for i in range(len(peaks) - 1):
            midpoint = (peaks[i] + peaks[i + 1]) // 2
            thresholds.append(midpoint)

        # Step 7: Apply thresholding 
        segmented = np.zeros_like(gray_image)

        if len(thresholds) == 1:
            t1 = thresholds[0]
            segmented[gray_image <= t1] = 0
            segmented[gray_image > t1] = 255

        elif len(thresholds) == 2:
            t1, t2 = thresholds
            segmented[gray_image <= t1] = 0
            segmented[(gray_image > t1) & (gray_image <= t2)] = 127
            segmented[gray_image > t2] = 255

        else:
            values = np.linspace(0, 255, len(thresholds) + 1, dtype=np.uint8)
            prev_thresh = 0
            for i, t in enumerate(thresholds):
                segmented[(gray_image > prev_thresh) & (gray_image <= t)] = values[i]
                prev_thresh = t
            segmented[gray_image > thresholds[-1]] = values[-1]

        return segmented

    @staticmethod
    def optimal_global(block):

        # Initialization:
        # corners=bg, others=obj
        height, width = block.shape
        iterations = 10
        output_block = block.copy()

        bg_mask = np.zeros_like(block, dtype=bool)
        bg_mask[0, 0] = True
        bg_mask[height - 1, 0] = True
        bg_mask[0, width - 1] = True
        bg_mask[height - 1, width - 1] = True
        obj_mask = ~bg_mask

        # Iterate:
        for i in range(iterations):
            obj_pixels = output_block[obj_mask]
            bg_pixels = output_block[bg_mask]

            # find mean of bg and obj pixel values
            obj_mean = np.mean(obj_pixels)
            bg_mean = np.mean(bg_pixels)

            # compute threshold (T) as their avg bg+obj/2  (avg of means)
            threshold = (obj_mean + bg_mean) / 2

            # clear the obj and bg pixels so they can be reused for the new values
            obj_mask = output_block > threshold
            bg_mask = output_block <= threshold

        output_block[output_block > threshold] = 255  # Set object pixels to white
        output_block[output_block <= threshold] = 0   # Set background pixels to black

        return output_block

    @staticmethod
    def optimal_local(image, block_size=30):
        # hane3mel 7war el window
        # w le kol wa7da haneb3atha 3al function w nraga3 el processed block
        height, width = image.shape
        output_image = np.zeros_like(image, dtype=np.int8)

        for i in range(0, height, block_size):
            for j in range(0, width, block_size):
                window = image[i:min(i + block_size, height), j:min(j + block_size, width)]
                thresholded_window = Thresholding.optimal_global(window)
                output_image[i:min(i + block_size, height), j:min(j + block_size, width)] = thresholded_window

        return output_image
