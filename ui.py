import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageViewerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        select_button = QPushButton("Select Image", self)
        select_button.clicked.connect(self.select_image)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(600, 400)  # Set a fixed size for the label

        enhance_brightness_contrast_button = QPushButton("Brightness and Contrast", self)
        enhance_brightness_contrast_button.clicked.connect(self.enhance_brightness_contrast)

        enhance_alpha_beta_button = QPushButton("Alpha and Beta", self)
        enhance_alpha_beta_button.clicked.connect(self.enhance_alpha_beta)

        sharpen_image_button = QPushButton("Sharpen Image", self)
        sharpen_image_button.clicked.connect(self.sharpen_image)

        laplacian_sharpening_button = QPushButton("Laplacian Sharpening", self)
        laplacian_sharpening_button.clicked.connect(self.laplacian_sharpening)

        median_blur_button = QPushButton("Median Blur", self)
        median_blur_button.clicked.connect(self.median_blur)

        gaussian_blur_button = QPushButton("Gaussian Blur", self)
        gaussian_blur_button.clicked.connect(self.gaussian_blur)

        enhance_colored_button = QPushButton("Enhance Colored", self)
        enhance_colored_button.clicked.connect(self.enhance_colored)

        original_image_button = QPushButton("Original Image", self)
        original_image_button.clicked.connect(self.show_original_image)

        quit_button = QPushButton("Quit", self)
        quit_button.clicked.connect(self.close)

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(enhance_brightness_contrast_button)
        button_layout.addWidget(enhance_alpha_beta_button)
        button_layout.addWidget(sharpen_image_button)
        button_layout.addWidget(laplacian_sharpening_button)
        button_layout.addWidget(median_blur_button)
        button_layout.addWidget(gaussian_blur_button)
        button_layout.addWidget(enhance_colored_button)
        button_layout.addWidget(original_image_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(select_button)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(quit_button)

        self.setLayout(main_layout)

        self.setWindowTitle("Image Viewer")

        # Set window size
        self.resize(800, 600)

        # Store the original image and enhanced image
        self.original_image = None
        self.enhanced_image = None

    def select_image(self):
        # Open file dialog to select an image
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Image files (*.png *.jpg *.jpeg)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]

            # Release resources of the previous original image and enhanced image
            if self.original_image is not None:
                del self.original_image
            if hasattr(self, 'enhanced_image') and self.enhanced_image is not None:
                del self.enhanced_image

            # Display the selected image
            self.original_image = cv2.imread(file_path)
            self.display_image(self.original_image)

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)  # Specify BGR888 format
        pixmap = QPixmap.fromImage(q_image)

        # Scale the image to fit the label while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

    def enhance_brightness_contrast(self):
        if self.original_image is not None:
            # Adjust brightness and contrast
            brightness = 10
            contrast = 2.3
            self.enhanced_image = cv2.addWeighted(self.original_image, contrast, np.zeros(self.original_image.shape, self.original_image.dtype), 0, brightness)

            # Display the enhanced image
            self.display_image(self.enhanced_image)

    def enhance_alpha_beta(self):
        if self.original_image is not None:
            # Adjust brightness and contrast using alpha and beta
            alpha = 1.5
            beta = 50
            self.enhanced_image = cv2.convertScaleAbs(self.original_image, alpha=alpha, beta=beta)

            # Display the enhanced image
            self.display_image(self.enhanced_image)

    def sharpen_image(self):
        if self.original_image is not None:
            # Create the sharpening kernel
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

            # Sharpen the image
            self.enhanced_image = cv2.filter2D(self.original_image, -1, kernel)

            # Display the enhanced image
            self.display_image(self.enhanced_image)

    def laplacian_sharpening(self):
        if self.original_image is not None:
            # Sharpen the image using the Laplacian operator
            self.enhanced_image = cv2.Laplacian(self.original_image, cv2.CV_64F)

            # Display the enhanced image
            self.display_image(self.enhanced_image)

    def median_blur(self):
        if self.original_image is not None:
            # Remove noise using a median filter
            self.enhanced_image = cv2.medianBlur(self.original_image, 11)

            # Display the enhanced image
            self.display_image(self.enhanced_image)

    def gaussian_blur(self):
        if self.original_image is not None:
            # Remove noise using a Gaussian filter
            self.enhanced_image = cv2.GaussianBlur(self.original_image, (7, 7), 0)

            # Display the enhanced image
            self.display_image(self.enhanced_image)

    def enhance_colored(self):
        if self.original_image is not None:
            # Convert the image from BGR to HSV color space
            image_hsv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)

            # Adjust the hue, saturation, and value of the image
            image_hsv[:, :, 0] = image_hsv[:, :, 0] * 0.7
            image_hsv[:, :, 1] = image_hsv[:, :, 1] * 1.5
            image_hsv[:, :, 2] = image_hsv[:, :, 2] * 0.5

            # Convert the image back to BGR color space
            self.enhanced_image = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

            # Display the enhanced image
            self.display_image(self.enhanced_image)

    def show_original_image(self):
        if self.original_image is not None:
            # Display the original image
            self.display_image(self.original_image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec_())