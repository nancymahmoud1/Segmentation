import numpy as np
import cv2


def kmeans_segmentation(image, k=3, maximum_iterations=100):
    # Step 1: Resize (keep it for now, practical)
    image = cv2.resize(image, (256, 256))

    # Step 2: Preprocess
    img_data = image.reshape((-1, 3)) if len(image.shape) == 3 else image.reshape((-1, 1))
    img_data = np.float32(img_data)

    # Step 3: Initialize random centroids
    np.random.seed(42)
    random_idxs = np.random.choice(len(img_data), k, replace=False)
    centroids = img_data[random_idxs]

    for iteration in range(maximum_iterations):
        # Step 4: Assignment step
        distances = np.linalg.norm(img_data[:, np.newaxis] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)

        # Step 5: Update step safely
        new_centroids = []
        for i in range(k):
            if np.any(labels == i):
                new_centroid = img_data[labels == i].mean(axis=0)
            else:
                # If no points assigned to this cluster, reinitialize randomly
                new_centroid = img_data[np.random.choice(len(img_data))]
            new_centroids.append(new_centroid)
        new_centroids = np.array(new_centroids)

        # Step 6: Convergence check
        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    # Step 7: Postprocess
    segmented_img = labels.reshape((image.shape[0], image.shape[1]))

    return segmented_img
