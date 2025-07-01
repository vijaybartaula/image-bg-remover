# Background Removal Tool

An interactive Python tool for removing backgrounds from images using advanced AI models, built with `rembg` and designed for Jupyter notebook environments.

## Features

- **One-Click Background Removal**: Upload an image and get instant background removal
- **Real-Time Preview**: See both original and processed images side-by-side
- **Transparency Preservation**: Outputs PNG format to maintain transparency
- **Interactive UI**: User-friendly interface with drag-and-drop upload
- **Automatic Saving**: Processed images are automatically saved with unique naming
- **Batch Processing**: Supports multiple images with automatic counter tracking

## Installation

### Prerequisites

- Python 3.7+
- Jupyter Notebook or Google Colab
- Internet connection (for initial model download)

### Dependencies

```bash
pip install rembg onnxruntime pillow ipywidgets markdown
```

### Quick Start

1. Copy the provided code into a Jupyter notebook cell
2. Run the cell to install dependencies and launch the interface
3. Upload an image using the file upload widget
4. View the processed result and download automatically

## Usage

### Basic Usage

1. **Upload Image**: Click the "Upload Image" button and select your image file
2. **Preview**: The original image will appear in the input preview
3. **Processing**: The tool automatically removes the background
4. **Result**: The processed image appears in the output preview
5. **Download**: The image is automatically saved to your system

Alternatively, you can download the file, upload it to your device, and run it with ease.

### Supported Formats

- **Input**: JPEG, PNG, BMP, TIFF, WebP
- **Output**: PNG (with transparency support)

### File Naming

Processed images are saved with the format: `output_image_[counter].png`

Example:
- First image: `output_image_1.png`
- Second image: `output_image_2.png`
- And so on...

## Technical Details

### Core Technology

- **rembg**: AI-powered background removal library
- **ONNX Runtime**: Optimized inference engine
- **PIL (Pillow)**: Image processing and manipulation
- **ipywidgets**: Interactive notebook widgets

### Model Architecture

The tool uses pre-trained neural networks optimized for background segmentation:
- **U²-Net**: Default model for general purpose background removal
- **ONNX Format**: Optimized for fast inference
- **GPU Acceleration**: Automatic GPU utilization when available

### Performance

- **Processing Time**: 2-5 seconds per image (depending on size and hardware)
- **Memory Usage**: ~200MB for model loading + image size
- **Resolution Support**: Up to 4K images (memory permitting)

## Configuration

### Advanced Options

You can customize the tool by modifying these variables:

```python
# Change output directory
output_directory = '/your/custom/path/'

# Modify image quality settings
quality_settings = {
    'format': 'PNG',
    'optimize': True,
    'compress_level': 6
}
```

### Model Selection

To use different rembg models:

```python
# Available models: u2net, u2netp, u2net_human_seg, silueta
from rembg import new_session
model = new_session('u2net_human_seg')  # Optimized for human subjects
```

## Troubleshooting

### Common Issues

**1. Installation Errors**
```bash
# Try upgrading pip first
pip install --upgrade pip
pip install rembg onnxruntime
```

**2. Memory Issues**
- Reduce image size before processing
- Close other applications to free memory
- Use Google Colab for better hardware resources

**3. Model Download Fails**
- Check internet connection
- Clear rembg cache: `rm -rf ~/.u2net`
- Restart notebook kernel

**4. Widget Display Issues**
```bash
# Enable jupyter widgets
jupyter nbextension enable --py widgetsnbextension
```

### Performance Optimization

- **Use GPU**: Install `onnxruntime-gpu` for faster processing
- **Batch Processing**: Process multiple images in sequence
- **Image Preprocessing**: Resize large images before processing

## Examples

### Basic Example

```python
from rembg import remove
from PIL import Image

# Process single image
with open('input.jpg', 'rb') as f:
    input_data = f.read()

output_data = remove(input_data)

with open('output.png', 'wb') as f:
    f.write(output_data)
```

### Custom Model Example

```python
from rembg import new_session, remove

# Use human-specific model
session = new_session('u2net_human_seg')
output_data = remove(input_data, session=session)
```

## Use Cases

- **E-commerce**: Product photography background removal
- **Social Media**: Profile picture editing
- **Design**: Creating transparent assets
- **Photography**: Portrait background replacement
- **Marketing**: Creating clean product images

## Limitations

- Processing time varies with image complexity
- Requires internet connection for initial model download
- Memory usage scales with image size
- May struggle with very complex backgrounds or fine details

## License

This project is built on open-source libraries:
- rembg: Apache License 2.0
- PIL: HPND License
- ipywidgets: BSD License

## Acknowledgments

- **rembg**: For providing the core background removal functionality
- **U²-Net**: For the underlying neural network architecture
- **ONNX**: For optimized model runtime
- **Jupyter**: For the interactive notebook environment
