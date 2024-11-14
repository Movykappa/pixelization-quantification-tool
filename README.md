# pixelization-quantification-tool
A tool to detect and quantify pixelization in images, including satellite imagery.
# Pixelization Quantification Tool

This tool helps detect pixelization in images based on an analysis of high-gradient regions and their horizontal/vertical alignment. It can be used to identify whether an image is overly pixelated, which can affect image quality for applications like super-resolution or enhancement processes.

## Description
The pixelization detection tool uses image processing techniques to analyze the structure of an image's high-gradient regions. The tool:

1. **Detects Gradient Magnitude**: Computes the gradient of the image to determine regions with high color or intensity changes.
2. **Skeletonizes High-Gradient Regions**: Extracts the central path of these regions, forming a skeleton to analyze.
3. **Evaluates Alignment**: Checks how much of the skeleton is composed of horizontal and vertical segments, which indicates pixelization.

## Key Features
- Applicable to **any type of image**, including natural photos, satellite imagery, medical images, etc.
- **Detects pixelation artifacts** by analyzing horizontal and vertical edges.
- Uses **gradient and skeletonization** techniques to evaluate the structural properties of the image.

## Limitations
- **Contrast Dependency**: The tool's accuracy is dependent on the presence of high contrast between different regions of the image. Low contrast images may lead to unreliable results.
- **Not Scientifically Validated**: This tool has not yet undergone extensive scientific validation across a broad set of image types or conditions.
- **Fixed Parameters**: Some of the parameters, such as the minimum length of line segments and gradient thresholds, are currently fixed and may need adjustment for specific use cases.

## Example Usage
To illustrate the tool's use, consider two images:
- One with **low pixelization**.

![Captura de ecrã 2024-11-14 181328](https://github.com/user-attachments/assets/517bf759-812c-40c1-9847-32f9277d08b6)

- One with **high pixelization**.
![Captura de ecrã 2024-11-14 181424](https://github.com/user-attachments/assets/20ef22d3-4b26-4854-a14a-65741c6f3704)
The tool will output a score indicating the extent of pixelization, which can be used to compare the two images.

In these two examples, the low pixelization image gives an aligned ratio of 24.3%, and the high pixelized image has an aligned ratio of 62.69%. 
Greater aligned ratio values are associated with greater pixelization of your image.

Please adapt your threshold to your specific application.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Movykappa/pixelization-quantification-tool.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script with the input image:
```bash
python pixelization-quantification-tool.py --image path/to/your/image.jpg
```

The output will include the pixelization score and a visualization of the detected high-gradient regions.

## Contribution
Contributions are welcome! Feel free to fork the repository and submit pull requests. Please include relevant test cases if adding new features.

## License
This project is licensed under the MIT License.

## Authors
- Mário Alberto Vieira - v1.0

