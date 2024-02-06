import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('images/city.jpg')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.show()

# Apply image enhancements
# Denoise the image
denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

# Perform contrast stretching
contrast_stretched_image = cv2.normalize(denoised_image, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)

# Image Sharpening
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
sharpened_image = cv2.filter2D(contrast_stretched_image, -1, kernel=kernel)

# Brightness Adjustment
brightness_image = cv2.convertScaleAbs(sharpened_image, alpha=1, beta=5)

# Gamma Correction
gamma = 1.5
lookup_table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
gamma_corrected_image = cv2.LUT(brightness_image, lookup_table)

# Save final image
cv2.imwrite('final_image.jpg', gamma_corrected_image)

# Display the final enhanced image
plt.imshow(cv2.cvtColor(gamma_corrected_image, cv2.COLOR_BGR2RGB))
plt.title('Final Enhanced Image')
plt.show()
