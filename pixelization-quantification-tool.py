import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
from skimage.measure import label
from math import atan2, degrees

# Function to analyze gradient regions and extract the skeleton
def analyze_gradient_paths(image, magnitude_threshold=50):
    # Convert to grayscale for analysis
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute the gradient magnitude using Sobel operators
    sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

    # Threshold the gradient magnitude to focus on strong gradients
    _, binary_mask = cv2.threshold(gradient_magnitude, magnitude_threshold, 255, cv2.THRESH_BINARY)
    binary_mask = binary_mask.astype(np.uint8)

    # Apply skeletonization to extract the midline
    skeleton = skeletonize(binary_mask // 255)  # Skeletonize expects binary image with values 0 and 1
    skeleton = (skeleton * 255).astype(np.uint8)  # Convert back to uint8 for visualization

    return gradient_magnitude, binary_mask, skeleton

# Function to compute skeleton properties: total length, horizontal/vertical length, and approximate horizontal/vertical length
def compute_skeleton_lengths(skeleton, min_length=10, angle_margin=2):
    # Get the coordinates of all skeleton points
    points = np.argwhere(skeleton > 0)

    total_length = 0
    aligned_length = 0

    current_segment = []
    for i in range(1, len(points)):
        y1, x1 = points[i - 1]
        y2, x2 = points[i]

        # Check if the point continues in a straight line
        if (y1 == y2 and abs(x2 - x1) == 1) or (x1 == x2 and abs(y2 - y1) == 1):
            current_segment.append((y2, x2))
        else:
            # Evaluate the length of the current segment
            if len(current_segment) >= min_length:
                segment_length = len(current_segment)
                total_length += segment_length

                # Calculate the angle of the segment
                delta_y = current_segment[-1][0] - current_segment[0][0]
                delta_x = current_segment[-1][1] - current_segment[0][1]
                angle = abs(degrees(atan2(delta_y, delta_x)))

                # Check if the segment is approximately aligned (either horizontal or vertical)
                if angle <= angle_margin or abs(angle - 90) <= angle_margin:
                    aligned_length += segment_length

            # Reset current segment
            current_segment = [(y2, x2)]

    # Evaluate the final segment
    if len(current_segment) >= min_length:
        segment_length = len(current_segment)
        total_length += segment_length

        # Calculate the angle of the segment
        delta_y = current_segment[-1][0] - current_segment[0][0]
        delta_x = current_segment[-1][1] - current_segment[0][1]
        angle = abs(degrees(atan2(delta_y, delta_x)))

        if angle <= angle_margin or abs(angle - 90) <= angle_margin:
            aligned_length += segment_length

    return total_length, aligned_length

# Function to plot the original image, gradient magnitude, binary mask, and skeleton side by side
def plot_image_with_skeleton(image, gradient_magnitude, binary_mask, skeleton, aligned_ratio, title):
    plt.figure(figsize=(24, 10))

    # Plotting the original image
    plt.subplot(1, 4, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f'{title}')
    plt.axis('off')

    # Plotting the gradient magnitude to visualize edges
    plt.subplot(1, 4, 2)
    plt.imshow(gradient_magnitude, cmap='hot')
    plt.title('Gradient Magnitude')
    plt.axis('off')

    # Plotting the binary mask to show high-gradient regions
    plt.subplot(1, 4, 3)
    plt.imshow(binary_mask, cmap='gray')
    plt.title('High-Gradient Regions')
    plt.axis('off')

    # Plotting the skeleton to show the midline of high-gradient regions
    plt.subplot(1, 4, 4)
    plt.imshow(skeleton, cmap='gray')
    plt.title(f'Skeleton - Aligned Ratio: {aligned_ratio:.2f}%')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

# Main function to evaluate images
def main():
    # Paths
    image_directory = "path/to/your/image/directory"

    # Iterate over images in the directory
    for image_name in os.listdir(image_directory):
        image_path = os.path.join(image_directory, image_name)
        if os.path.isfile(image_path):
            # Load the image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image: {image_name}")
                continue

            # Analyze gradient regions and extract the skeleton
            gradient_magnitude, binary_mask, skeleton = analyze_gradient_paths(image)

            # Compute the skeleton lengths
            total_length, aligned_length = compute_skeleton_lengths(skeleton)
            aligned_ratio = (aligned_length / total_length) * 100 if total_length > 0 else 0

            # Plot the image, gradient magnitude, binary mask, and skeleton side by side
            plot_image_with_skeleton(image, gradient_magnitude, binary_mask, skeleton, aligned_ratio, f"Image: {image_name}")

            # Output aligned ratio
            print(f"Image: {image_name}, Aligned Ratio: {aligned_ratio:.2f}%")

if __name__ == "__main__":
    main()
