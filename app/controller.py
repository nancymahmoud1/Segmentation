import numpy as np
from PyQt5 import QtWidgets, QtCore

# Core utility and services
from app.utils.clean_cache import remove_directories
from app.utils.logging_manager import LoggingManager
from app.services.image_service import ImageServices

# Main GUI design
from app.design.main_layout import Ui_MainWindow
from app.processing.segmentation_clusters import kMeans_segmentation, agglomerative_segmentation
from app.processing.thresholding import Thresholding
from app.processing.segmentation import ImageSegmenter
# Image processing functionality
import cv2


class MainWindowController:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()

        self.path = None
        self.path_1 = None
        self.path_2 = None

        self.original_image = None
        self.processed_image = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.log = LoggingManager()

        self.srv = ImageServices()
        self.segmenter = ImageSegmenter()

        # Connect signals to slots
        self.setupConnections()

    def run(self):
        """Run the application."""
        self.MainWindow.showFullScreen()
        self.app.exec_()

    def setupConnections(self):
        """Connect buttons to their respective methods."""
        self.ui.quit_app_button.clicked.connect(self.closeApp)
        self.ui.upload_button.clicked.connect(self.drawImage)

        self.ui.save_image_button.clicked.connect(lambda: self.srv.save_image(self.processed_image))
        self.ui.clear_image_button.clicked.connect(self.clear_images)
        self.ui.reset_image_button.clicked.connect(self.reset_images)

        # Thresholding connections
        self.ui.thresholding_button.clicked.connect(self.show_thresholding_controls)
        self.ui.thresholding_back_button.clicked.connect(self.show_main_buttons)
        self.ui.optimal_button.clicked.connect(lambda: self.apply_thresholding(Thresholding.optimal_thresholding))
        self.ui.spectral_threshold_apply_button.clicked.connect(lambda: self.apply_thresholding(Thresholding.spectral_thresholding))
        self.ui.otsu_button.clicked.connect(lambda: self.apply_thresholding(Thresholding.otsu_thresholding))

        # Segmentation connections
        self.ui.segmentation_button.clicked.connect(self.show_segmentation_controls)
        self.ui.seg_back_button.clicked.connect(self.show_main_buttons)
        self.ui.apply_kMeans_clustering_button.clicked.connect(self.apply_k_mean_clustering)
        self.ui.apply_agglomerative_clustering_button.clicked.connect(self.apply_agglomerative_clustering)

        # New segmentation methods
        self.ui.region_growing_button.clicked.connect(self.apply_region_growing)
        self.ui.mean_shift_button.clicked.connect(self.apply_mean_shift)
        self.ui.region_growing_tolerance_slider.valueChanged.connect(self.update_region_growing_tolerance)

        # Mouse click for seed point
        self.ui.original_groupBox.mousePressEvent = self.get_seed_point

    def drawImage(self):
        self.path = self.srv.upload_image_file()

        if not self.path:
            return

        self.original_image = cv2.imread(self.path)
        if self.original_image is None:
            return

        self.processed_image = self.original_image.copy()

        # Clear any existing images displayed in the group boxes
        self.srv.clear_image(self.ui.original_groupBox)
        self.srv.clear_image(self.ui.processed_groupBox)

        # Display the images in their respective group boxes
        self.srv.set_image_in_groupbox(self.ui.original_groupBox, self.original_image)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

        # Show the group boxes if they're hidden
        self.ui.original_groupBox.show()
        self.ui.processed_groupBox.show()

    def apply_k_mean_clustering(self):
        k = self.ui.clusters_number_slider.value()
        segmented_labels = kMeans_segmentation(self.original_image.copy(), k)

        # Colorize the segmentation
        segmented_display = cv2.applyColorMap(
            (segmented_labels * int(255 / (k - 1))).astype(np.uint8),
            cv2.COLORMAP_JET
        )

        self.processed_image = segmented_display
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def apply_agglomerative_clustering(self):
        k = self.ui.clusters_number_slider.value()  # Get number of clusters from the slider

        segmented_labels = agglomerative_segmentation(self.original_image.copy(), k)

        # Colorize the segmentation result for display
        segmented_display = cv2.applyColorMap(
            (segmented_labels * int(255 / (k - 1))).astype(np.uint8),
            cv2.COLORMAP_JET
        )

        self.processed_image = segmented_display
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)


    def update_region_growing_tolerance(self):
        """Update tolerance value from slider."""
        self.segmenter.set_tolerance(self.ui.region_growing_tolerance_slider.value())

    def update_bandwidth_mean_shift(self):
        self.segmenter.set_bandwidth(self.ui.mean_shift_bandwidth_slider.value())

    def update_spatial_radius_mean_shift(self):
        self.segmenter.set_spatial_radius(self.ui.spatial_length_slider.value())

    def get_seed_point(self, event):
        """Handle mouse click to set seed point for region growing."""
        if self.original_image is None:
            return

        # Get the label widget that displays the image
        label = self.ui.processed_groupBox.findChild(QtWidgets.QLabel)
        if not label or label.pixmap() is None:
            return

        # Calculate position in image coordinates
        pixmap = label.pixmap()
        pos = event.pos()

        # Scale coordinates from widget to image
        x = int(pos.x() * (self.original_image.shape[1] / pixmap.width()))
        y = int(pos.y() * (self.original_image.shape[0] / pixmap.height()))

        # Ensure coordinates are within bounds
        x = max(0, min(x, self.original_image.shape[1] - 1))
        y = max(0, min(y, self.original_image.shape[0] - 1))

        self.segmenter.set_seed_point((y, x))
        print(f"Seed point set to: {(y, x)}")

    def apply_region_growing(self):
        """Apply region growing segmentation."""
        if self.original_image is None:
            return

        try:
            segmented = self.segmenter.region_growing(self.original_image)
            self.processed_image = cv2.cvtColor(segmented, cv2.COLOR_GRAY2BGR)
            self.showProcessed()
        except ValueError as e:
            print(str(e))
            QtWidgets.QMessageBox.warning(self.MainWindow, "Error", str(e))

    def apply_mean_shift(self):
        """Apply mean shift segmentation."""
        if self.original_image is None:
            return

        # Show busy cursor during processing
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            self.processed_image = self.segmenter.mean_shift(self.original_image)
            self.showProcessed()
        except Exception as e:
            print(str(e))
            QtWidgets.QMessageBox.warning(self.MainWindow, "Error", str(e))
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def apply_thresholding(self, thresholding_method, mode="Global", block_size=30):
        # ensure image is grayscale
        gray_image=cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        # extract parameters
        mode = self.ui.threshold_type_combo.currentText()
        block_size=self.ui.block_size_slider.value()

        # call the appropriate function based on mode
        if mode=="Global":
            self.processed_image=thresholding_method(gray_image)
        elif mode=="Local":
            self.processed_image=Thresholding.local_thresholding(gray_image, thresholding_method, block_size)

        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def apply_spectral_thresholding(self):
        segmented_image = Thresholding.spectral_thresholding(self.original_image.copy())

        self.processed_image = segmented_image
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def clear_images(self):
        if self.original_image is None:
            return

        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.clear_image(self.ui.original_groupBox)

    def reset_images(self):
        if self.original_image is None:
            return

        self.processed_image = self.original_image.copy()
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.original_image)

    def showProcessed(self):
        if self.processed_image is None:
            print("Error: Processed image is None.")
            return

        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    # Thresholding methods
    def show_thresholding_controls(self):
        self.ui.sidebar_stacked.setCurrentIndex(1)

    # Segmentation methods
    def show_segmentation_controls(self):
        self.ui.sidebar_stacked.setCurrentIndex(2)

    def closeApp(self):
        """Close the application."""
        remove_directories()
        self.app.quit()

    def show_main_buttons(self):
        """Switch back to the main buttons page and hide the image group boxes."""
        self.ui.sidebar_stacked.setCurrentIndex(0)
