import numpy as np
import cv2
from scipy.signal import find_peaks


def spectral_thresholding(image):
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image.copy()

    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256]).flatten()
    hist_smooth = cv2.GaussianBlur(hist.reshape(-1, 1), (5, 5), 0).flatten()

    peaks, _ = find_peaks(hist_smooth, distance=20, prominence=0.01 * np.max(hist_smooth))

    if len(peaks) < 2:
        # Not enough peaks found, apply simple Otsu thresholding as fallback
        _, segmented = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return segmented

    thresholds = []
    for i in range(len(peaks) - 1):
        midpoint = (peaks[i] + peaks[i + 1]) // 2
        thresholds.append(midpoint)

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
