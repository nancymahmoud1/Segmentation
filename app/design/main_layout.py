from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from app.design.tools.gui_utilities import GUIUtilities


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.screen_size = QtWidgets.QApplication.primaryScreen().size()
        MainWindow.resize(self.screen_size.width(), self.screen_size.height())

        # 1) Define style variables
        self.setupStyles()
        self.util = GUIUtilities()

        # 2) Apply main window style
        MainWindow.setStyleSheet(self.main_window_style)

        # 3) Central widget & main layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.main_vertical_layout.setSpacing(0)

        # 4) Create Title (icon + label) and Navbar (upload, reset, save, quit)
        self.setupTitleArea()
        self.setupNavbar()
        self.combineTitleAndNavbar()

        # Add the top bar (title+navbar) to the main vertical layout
        self.main_vertical_layout.addLayout(self.title_nav_layout)

        # 5) Create the main content: left sidebar + two group boxes on the right
        self.setupMainContent()
        self.main_vertical_layout.addLayout(self.main_content_layout)

        # 6) Finalize the main window
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu bar & status bar (if needed)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.original_groupBox.show()
        self.processed_groupBox.show()

        # 7) Set window title, etc.
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ----------------------------------------------------------------------
    # Styles
    # ----------------------------------------------------------------------
    def setupStyles(self):
        """Holds all style sheets in one place for easier modification."""
        self.main_window_style = """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
        """

        self.button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f3460, stop:1 #16213e);
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 8px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #16213e, stop:1 #0f3460);
                border: 1px solid #e94560;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f3460, stop:1 #16213e);
                padding-top: 13px;
                padding-bottom: 11px;
            }
        """

        self.quit_button_style = """
            QPushButton {
                background: transparent;
                color: #e94560;
                border: 2px solid #e94560;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e94560;
                color: white;
                border: 2px solid #e94560;
            }
        """

        self.groupbox_style = """
            QGroupBox {
                color: white;
                border: 2px solid #0f3460;
                border-radius: 12px;
                margin-top: 16px;
                font-weight: bold;
                padding-top: 16px;
                background: rgba(15, 52, 96, 0.2);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                color: #e94560;
            }
        """

        self.slider_style = """
            QSlider::groove:horizontal {
                border: 1px solid #0f3460;
                height: 6px;
                background: #16213e;
                margin: 2px 0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e94560, stop:1 #0f3460);
                width: 20px;
                margin: -8px 0;
                border-radius: 6px;
                border: 2px solid #16213e;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e94560, stop:1 #0f3460);
                border: 1px solid #0f3460;
                height: 6px;
                border-radius: 3px;
            }
        """

        self.label_style = """
            QLabel {
                color: white;
                font-size: 14px;
                padding: 6px;
                font-weight: bold;
            }
        """

        self.back_icon_path = "static/icons/Back-icon.png"

    # ----------------------------------------------------------------------
    # Title + Navbar
    # ----------------------------------------------------------------------
    def setupTitleArea(self):
        """Creates the title icon & label in a horizontal layout."""
        self.title_icon = QtWidgets.QLabel()
        self.title_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.title_icon.setPixmap(QtGui.QPixmap("static/icons/icon.png"))
        self.title_icon.setScaledContents(True)
        self.title_icon.setObjectName("title_icon")

        self.title_label = self.util.createLabel(
            text="SegmaVision",
            style="color:white; padding:10px; padding-left:0; font-size: 32px; font-weight: bold",
            isHead=True
        )
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(32)
        font.setBold(True)
        self.title_label.setFont(font)

        # Vertical layout for title and subtitle
        title_layout = QtWidgets.QVBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.setSpacing(0)

        # Horizontal layout for icon + title group
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.addWidget(self.title_icon)
        self.title_layout.addLayout(title_layout)

    def setupNavbar(self):
        """Creates the Upload, Reset, Save, and Quit buttons."""
        self.upload_button = self.util.createButton("📁 Upload Image", self.button_style)
        self.reset_image_button = self.util.createButton("🔄 Reset", self.button_style)
        self.save_image_button = self.util.createButton("💾 Save", self.button_style)
        self.clear_image_button = self.util.createButton("🗑️ Clear", self.button_style)

        self.quit_app_button = self.util.createButton("X", self.quit_button_style)
        self.util.adjust_quit_button(self.quit_app_button)

        self.navbar_layout = QtWidgets.QHBoxLayout()
        self.navbar_layout.setSpacing(15)
        self.navbar_layout.addWidget(self.upload_button)
        self.navbar_layout.addWidget(self.reset_image_button)
        self.navbar_layout.addWidget(self.save_image_button)
        self.navbar_layout.addWidget(self.clear_image_button)
        self.navbar_layout.addWidget(self.quit_app_button)

    def combineTitleAndNavbar(self):
        """Combines the title & navbar in one horizontal layout."""
        self.title_nav_layout = QtWidgets.QHBoxLayout()
        self.title_nav_layout.addLayout(self.title_layout)
        self.title_nav_layout.addStretch(1)
        self.title_nav_layout.addLayout(self.navbar_layout)

    # ----------------------------------------------------------------------
    # Main Content: Sidebar + GroupBoxes
    # ----------------------------------------------------------------------
    def setupMainContent(self):
        """
        Creates a horizontal layout that includes:
         - A stacked sidebar (main buttons vs. noise controls)
         - Two group boxes (Original & Processed) side-by-side
        """
        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setSpacing(10)

        # 1) Sidebar (QStackedWidget)
        self.setupSidebarStack()
        self.main_content_layout.addWidget(self.sidebar_stacked)

        # 2) Group Boxes
        self.setupImageGroupBoxes()
        images_layout = QtWidgets.QHBoxLayout()
        images_layout.setSpacing(10)
        images_layout.addWidget(self.original_groupBox)
        images_layout.addWidget(self.processed_groupBox)

        self.main_content_layout.addLayout(images_layout)

    # ----------------------------------------------------------------------
    # Sidebar with QStackedWidget
    # ----------------------------------------------------------------------
    def setupSidebarStack(self):
        """
        Creates a QStackedWidget with two pages:
          Page 0 = main sidebar buttons
          Page 1 = thresholding controls
          Page 2 = segmentation controls
        """
        # The stacked widget
        self.sidebar_stacked = QtWidgets.QStackedWidget()
        self.sidebar_stacked.setMinimumWidth(250)  # Adjust as needed

        # PAGE 0: Main Buttons
        self.page_main_buttons = QtWidgets.QWidget()
        self.page_main_buttons_layout = QtWidgets.QVBoxLayout(self.page_main_buttons)
        self.page_main_buttons_layout.setSpacing(25)

        self.setupMainButtons()  # Creates the main buttons
        # Add them to the page_main_buttons_layout
        for btn in self.MAIN_BUTTONS:
            self.page_main_buttons_layout.addWidget(btn)

        self.sidebar_stacked.addWidget(self.page_main_buttons)

        # PAGE 1: Thresholding Controls
        self.page_thresholding_controls = QtWidgets.QWidget()
        self.page_thresholding_layout = QtWidgets.QVBoxLayout(self.page_thresholding_controls)
        self.page_thresholding_layout.setSpacing(10)

        # Add thresholding widgets
        self.setupThresholdingWidgets()
        self.sidebar_stacked.addWidget(self.page_thresholding_controls)

        # PAGE 2: Segmentation Controls
        self.page_segmentation_controls = QtWidgets.QWidget()
        self.page_segmentation_layout = QtWidgets.QVBoxLayout(self.page_segmentation_controls)
        self.page_segmentation_layout.setSpacing(10)

        # Add segmentation widgets
        self.setupSegmentationWidgets()
        self.sidebar_stacked.addWidget(self.page_segmentation_controls)

        # By default, show page 0
        self.sidebar_stacked.setCurrentIndex(0)

    def setupMainButtons(self):
        """Creates the main sidebar buttons."""
        self.thresholding_button = self.util.createButton("Thresholding", self.button_style)
        self.segmentation_button = self.util.createButton("Segmentation", self.button_style)

        self.MAIN_BUTTONS = [
            self.thresholding_button,
            self.segmentation_button
        ]

    def setupImageGroupBoxes(self):
        """Creates two group boxes: Original Image & Processed Image."""
        self.original_groupBox, _ = self.util.createGroupBox(
            title="Original Image",
            size=QtCore.QSize(int(self.screen_size.width() * (502 / 1280)),
                              int(self.screen_size.height() * (526 / 800))),
            style=self.groupbox_style,
            isGraph=False
        )
        self.processed_groupBox, _ = self.util.createGroupBox(
            title="Processed Image",
            size=QtCore.QSize(int(self.screen_size.width() * (502 / 1280)),
                              int(self.screen_size.height() * (526 / 800))),
            style=self.groupbox_style,
            isGraph=False
        )

    def setupThresholdingWidgets(self):
        """Setup widgets for thresholding controls with proper attribute creation"""
        # Create the container widget if it doesn't exist
        if not hasattr(self, 'page_thresholding_controls'):
            self.page_thresholding_controls = QtWidgets.QWidget()

        # Clear any existing layout
        if hasattr(self, 'page_thresholding_layout'):
            QtWidgets.QWidget().setLayout(self.page_thresholding_layout)

        # Create new layout with consistent spacing
        self.page_thresholding_layout = QtWidgets.QVBoxLayout(self.page_thresholding_controls)
        self.page_thresholding_layout.setSpacing(30)
        self.page_thresholding_layout.setContentsMargins(10, 10, 10, 10)

        # Create and store buttons as attributes
        # Create and store buttons as attributes
        self.thresholding_back_button = self.util.createButton("", self.quit_button_style)
        self.thresholding_back_button.setIcon(QIcon(self.back_icon_path))
        self.thresholding_back_button.setIconSize(QSize(50, 50))
        # Add threshold type selection (Local/Global)
        self.threshold_type_label = self.util.createLabel("Threshold Type:", "color: white; font-weight: bold;")
        self.threshold_type_combo = QtWidgets.QComboBox()
        self.threshold_type_combo.addItems(["Global", "Local"])
        self.threshold_type_combo.setStyleSheet("""
            QComboBox {
                background: #16213e;
                color: white;
                border: 1px solid #0f3460;
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox:hover {
                border: 1px solid #e94560;
            }
        """)

        # Create value display labels for sliders
        self.block_size_value_label = self.util.createLabel("30", "color: #e94560; font-weight: bold;")

        # Create horizontal layouts for slider value displays
        block_size_layout = QtWidgets.QHBoxLayout()
        block_size_layout.addWidget(self.util.createLabel("Block Size:", "color: white;"))
        block_size_layout.addWidget(self.block_size_value_label)



        self.otsu_button = self.util.createButton("Otsu Thresholding", self.button_style)
        self.optimal_button = self.util.createButton("Optimal Thresholding", self.button_style)
        self.spectral_threshold_apply_button = self.util.createButton("Spectral Thresholding", self.button_style)

        # Add widgets to layout
        self.page_thresholding_layout.addWidget(self.thresholding_back_button)
        self.page_thresholding_layout.addWidget(self.util.createSeparator())
        self.page_thresholding_layout.addWidget(self.threshold_type_label)
        self.page_thresholding_layout.addWidget(self.threshold_type_combo)
        self.page_thresholding_layout.addWidget(self.util.createSeparator())
        self.page_thresholding_layout.addWidget(self.otsu_button)
        self.page_thresholding_layout.addWidget(self.optimal_button)
        self.page_thresholding_layout.addWidget(self.spectral_threshold_apply_button)
        self.page_thresholding_layout.addWidget(self.util.createSeparator())

        # Create and add sliders
        self.block_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.block_size_slider.setRange(2, 100)
        self.block_size_slider.setValue(30)
        self.block_size_slider.setSingleStep(2)
        self.block_size_slider.setStyleSheet(self.slider_style)


        # Add slider widgets with their value displays
        self.page_thresholding_layout.addLayout(block_size_layout)
        self.page_thresholding_layout.addWidget(self.block_size_slider)

        # Connect slider signals to update the value labels
        self.block_size_slider.valueChanged.connect(lambda val: self.block_size_value_label.setText(str(val)))

        # Add stretch to push content up
        self.page_thresholding_layout.addStretch(1)

        # Add to stacked widget if not already added
        if self.page_thresholding_controls not in [self.sidebar_stacked.widget(i) for i in
                                                   range(self.sidebar_stacked.count())]:
            self.sidebar_stacked.addWidget(self.page_thresholding_controls)

    def setupSegmentationWidgets(self):
        """Setup widgets for segmentation controls with proper attribute creation"""
        # Create the container widget if it doesn't exist
        if not hasattr(self, 'page_segmentation_controls'):
            self.page_segmentation_controls = QtWidgets.QWidget()

        # Clear any existing layout
        if hasattr(self, 'page_segmentation_layout'):
            QtWidgets.QWidget().setLayout(self.page_segmentation_layout)

        # Create new layout with consistent spacing
        self.page_segmentation_layout = QtWidgets.QVBoxLayout(self.page_segmentation_controls)
        self.page_segmentation_layout.setSpacing(22)
        self.page_segmentation_layout.setContentsMargins(10, 10, 10, 10)

        # Create and store buttons as attributes
        # Create and store buttons as attributes
        self.seg_back_button = self.util.createButton("", self.quit_button_style)
        self.seg_back_button.setIcon(QIcon(self.back_icon_path))
        self.seg_back_button.setIconSize(QSize(50, 50))
        self.apply_kMeans_clustering_button = self.util.createButton("K-means", self.button_style)
        self.region_growing_button = self.util.createButton("Region Growing", self.button_style)
        self.mean_shift_button = self.util.createButton("Mean Shift", self.button_style)
        self.apply_agglomerative_clustering_button = self.util.createButton("Agglomerative", self.button_style)

        # Create value display labels for sliders
        self.kmeans_clusters_value = self.util.createLabel("3", "color: #e94560; font-weight: bold;")
        self.region_threshold_value = self.util.createLabel("20", "color: #e94560; font-weight: bold;")
        self.spatial_raduis_value = self.util.createLabel("15", "color: #e94560; font-weight: bold;")
        self.mean_shift_bandwidth_value = self.util.createLabel("30", "color: #e94560; font-weight: bold;")

        # Create horizontal layouts for slider value displays
        kmeans_layout = QtWidgets.QHBoxLayout()
        kmeans_layout.addWidget(self.util.createLabel("Number of Clusters:", "color: white;"))
        kmeans_layout.addWidget(self.kmeans_clusters_value)

        region_layout = QtWidgets.QHBoxLayout()
        region_layout.addWidget(self.util.createLabel("Tolerance - Region Growing:", "color: white;"))
        region_layout.addWidget(self.region_threshold_value)

        spatial_layout = QtWidgets.QHBoxLayout()
        spatial_layout.addWidget(self.util.createLabel("Spatial Radius:", "color: white;"))
        spatial_layout.addWidget(self.spatial_raduis_value)

        bandwidth_layout = QtWidgets.QHBoxLayout()
        bandwidth_layout.addWidget(self.util.createLabel("Bandwidth- Mean Shift:", "color: white;"))
        bandwidth_layout.addWidget(self.mean_shift_bandwidth_value)

        # Create and add sliders
        self.clusters_number_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.clusters_number_slider.setRange(2, 10)
        self.clusters_number_slider.setValue(3)
        self.clusters_number_slider.setStyleSheet(self.slider_style)

        self.region_growing_tolerance_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.region_growing_tolerance_slider.setRange(1, 50)
        self.region_growing_tolerance_slider.setValue(20)
        self.region_growing_tolerance_slider.setStyleSheet(self.slider_style)

        self.mean_shift_bandwidth_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.mean_shift_bandwidth_slider.setRange(5, 50)
        self.mean_shift_bandwidth_slider.setValue(20)
        self.mean_shift_bandwidth_slider.setStyleSheet(self.slider_style)

        self.spatial_length_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spatial_length_slider.setRange(10, 30)
        self.spatial_length_slider.setValue(15)
        self.spatial_length_slider.setStyleSheet(self.slider_style)

        # Add buttons to layout
        self.page_segmentation_layout.addWidget(self.seg_back_button)
        self.page_segmentation_layout.addWidget(self.util.createSeparator())
        # Add widgets to layout with their value displays
        self.page_segmentation_layout.addLayout(kmeans_layout)
        self.page_segmentation_layout.addWidget(self.clusters_number_slider)
        self.page_segmentation_layout.addWidget(self.apply_kMeans_clustering_button)
        self.page_segmentation_layout.addWidget(self.apply_agglomerative_clustering_button)
        self.page_segmentation_layout.addWidget(self.util.createSeparator())


        self.page_segmentation_layout.addLayout(region_layout)
        self.page_segmentation_layout.addWidget(self.region_growing_tolerance_slider)

        self.page_segmentation_layout.addWidget(self.region_growing_button)

        self.page_segmentation_layout.addLayout(bandwidth_layout)
        self.page_segmentation_layout.addWidget(self.mean_shift_bandwidth_slider)
        self.page_segmentation_layout.addLayout(spatial_layout)
        self.page_segmentation_layout.addWidget(self.spatial_length_slider)
        self.page_segmentation_layout.addWidget(self.mean_shift_button)

        # Connect slider signals to update the value labels
        self.clusters_number_slider.valueChanged.connect(lambda val: self.kmeans_clusters_value.setText(str(val)))
        self.spatial_length_slider.valueChanged.connect(lambda val: self.spatial_raduis_value.setText(str(val)))
        self.region_growing_tolerance_slider.valueChanged.connect(lambda val: self.region_threshold_value.setText(str(val)))
        self.mean_shift_bandwidth_slider.valueChanged.connect(
            lambda val: self.mean_shift_bandwidth_value.setText(str(val)))

        # Add stretch to push content up
        self.page_segmentation_layout.addStretch(1)

        # Add to stacked widget if not already added
        if self.page_segmentation_controls not in [self.sidebar_stacked.widget(i) for i in
                                                   range(self.sidebar_stacked.count())]:
            self.sidebar_stacked.addWidget(self.page_segmentation_controls)
    # ----------------------------------------------------------------------
    # Retranslate
    # ----------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    # ----------------------------------------------------------------------
    #  Show/Hide Logic
    # ----------------------------------------------------------------------
    def show_main_buttons(self):
        """
        Switches back to the main buttons page, shows the original and processed group boxes,
        and hides the hybrid image group boxes.
        """
        # Show the original and processed group boxes
        self.original_groupBox.show()
        self.processed_groupBox.show()

        # Switch to the main buttons page
        self.sidebar_stacked.setCurrentIndex(0)
