import time

import numpy as np
import cv2
from collections import deque


class ImageSegmenter:
    def __init__(self):
        # Region Growing
        self.seed_point = None
        self.tolerance = 20

        # Mean shift parameters
        self.bandwidth = 30
        self.spatial_radius = 15
        self.max_iterations = 10

    # Set Region Growing Parameters
    def set_seed_point(self, point):
        self.seed_point = point

    def set_tolerance(self, tolerance):
        self.tolerance = tolerance

    # Set parameters for mean shift.
    def set_mean_shift_params(self, bandwidth, spatial_radius, max_iterations):
        self.bandwidth = bandwidth
        self.spatial_radius = spatial_radius
        self.max_iterations = max_iterations

    def region_growing(self, image):

        if self.seed_point is None:
            raise ValueError("Seed point not set")

        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        height, width = image.shape
        segmented = np.zeros((height, width), dtype=np.uint8)
        visited = np.zeros((height, width), dtype=bool)

        seed_value = image[self.seed_point]
        queue = deque([self.seed_point])
        visited[self.seed_point] = True

        while queue:
            y, x = queue.popleft()
            segmented[y, x] = 255

            # Check 8-connected neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue

                    ny, nx = y + dy, x + dx

                    if 0 <= ny < height and 0 <= nx < width and not visited[ny, nx]:
                        pixel_value = image[ny, nx]
                        if abs(int(pixel_value) - int(seed_value)) <= self.tolerance:
                            visited[ny, nx] = True
                            queue.append((ny, nx))

        return segmented    # Segmented image as binary mask

    def mean_shift(self, image):
        """Mean shift segmentation using sliding window """

        start = time.perf_counter()

        # # Convert to LUV color space
        # luv_image = cv2.cvtColor(image, cv2.COLOR_BGR2LUV).astype(np.float32)
        # height, width = luv_image.shape[:2]
        # segmented = np.zeros_like(luv_image)

        # Downsample the image (e.g., half resolution)
        scale_factor = 0.5
        small_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

        # Process the smaller image
        small_luv = cv2.cvtColor(small_image, cv2.COLOR_BGR2LUV).astype(np.float32)
        height, width = small_luv.shape[:2]
        segmented_small = np.zeros_like(small_luv)

        # Precompute spatial grid
        y_coords, x_coords = np.indices((height, width))

        for y in range(height):
            for x in range(width):
                current_color = small_luv[y, x]
                current_pos = np.array([y, x], dtype=np.float32)
                mean_color = current_color.copy()
                mean_pos = current_pos.copy()

                for _ in range(self.max_iterations):
                    # Compute spatial and color distances
                    spatial_dist_sq = (y_coords - mean_pos[0]) ** 2 + (x_coords - mean_pos[1]) ** 2
                    color_dist_sq = np.sum((small_luv - mean_color) ** 2, axis=2)
                    mask = (spatial_dist_sq <= self.spatial_radius ** 2) & (color_dist_sq <= self.bandwidth ** 2)
                    if not np.any(mask):
                        break

                    # Update mean
                    window_pixels = small_luv[mask]
                    window_y = y_coords[mask]
                    window_x = x_coords[mask]

                    new_mean_color = np.mean(window_pixels, axis=0)
                    new_mean_pos = np.array([
                        np.mean(window_y),
                        np.mean(window_x)
                    ])

                    # Check convergence
                    if (np.linalg.norm(new_mean_color - mean_color) < 1 and
                            np.linalg.norm(new_mean_pos - mean_pos) < 1):
                        break

                    mean_color = new_mean_color
                    mean_pos = new_mean_pos

                segmented_small[y, x] = mean_color

        # Convert back to BGR
        segmented_small = cv2.cvtColor(segmented_small.astype(np.uint8), cv2.COLOR_LUV2BGR)

        # Upsample the result to original size
        segmented = cv2.resize(segmented_small, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LINEAR)

        end = time.perf_counter()
        print(f"Mean shift executed in {end - start:.4f} seconds")
        return segmented