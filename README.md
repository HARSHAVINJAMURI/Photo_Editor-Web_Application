# Photo Editor Web App

This is a **Streamlit-based Photo Editor Web Application** built with Python. It allows users to upload an image and perform various editing operations including filters, sky styles, aspect ratio cropping, text addition, brightness/contrast adjustments, and color channel visualization. Users can also download the edited image, color channels, or colormapped images.

---

## Features

### 1. Image Upload
- Supports `.jpg`, `.jpeg`, and `.png` formats.
- Displays the original uploaded image.

### 2. Image Rotation
- Rotate images by **0°, 90°, 180°, 270°**.

### 3. Aspect Ratio Crop
- Crop the image to preset ratios:
  - `1:1`, `4:3`, `16:9`, `9:16`, `3:2`, `21:9`
- Supports **horizontal and vertical offset** to choose which part of the image to keep.
- Automatically fills extra space with **white background** if needed.

### 4. Adjusting Tools
- **Brightness**, **Contrast**, **Sharpness**, **Saturation** sliders.
- **Vignette effect** to add stylish focus.

### 5. Add Text
- Add custom text to the image.
- Options include:
  - Font size, text color.
  - Horizontal and vertical offsets.
  - 15 stylish system fonts like Arial, Verdana, Tahoma, Impact, Comic Sans MS, etc.

### 6. Filters
- Apply popular filters:
  - Invert Colors, Grayscale, Old Film (Sepia), Outlines, Warm Tone, Cool Tone, Vintage Fade, High Contrast, Soft Pastel.
- Adjust **Filter Intensity**.

### 7. Sky Styles
- Enhance sky appearance with:
  - Bright Day, Golden Hour, Sunset Glow, Night Sky, Stormy Mood.
- Adjust **Sky Style Intensity**.

### 8. Color Channels
- Visualize **Red, Green, and Blue channels** individually.
- Download each channel separately.

### 9. Colormapped Image
- Convert image to grayscale and apply a **wide variety of matplotlib colormaps**.
- Preview and download colormapped image.
- Examples of colormaps: `viridis`, `plasma`, `inferno`, `magma`, `cividis`, `hot`, `cool`, `spring`, `autumn`, and more.

### 10. Download Options
- Download **Edited Image** with a custom filename.
- Separate download buttons for **Color Channels** and **Colormap** images.

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/photo-editor-webapp.git
```
2. Navigate to the project folder:
```bash
cd photo-editor-webapp
```
3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## How to Run
```bash
streamlit run app.py
```
- The app will open in your default browser.
- Upload your image and start editing.

## Dependencies
- Python 3.8+
- Streamlit
- Pillow
- NumPy
- Matplotlib

## License
This project is licensed under the MIT License. See the LICENSE
 file for details.

## Author
- Vinajmuri Harsha
- GitHub: https://github.com/HARSHAVINJAMURI
- Email: vinjamuriharsh123@gmail.com
---









