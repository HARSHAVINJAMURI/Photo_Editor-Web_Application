import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter , ImageOps, ImageDraw, ImageFont
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.pyplot as plt 
from io import BytesIO  

st.set_page_config(page_title="Photo Editor", layout="centered")
st.title("Photo Editor Web App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
else:
    st.warning("Please upload an image file.")
    st.stop()

st.image(image, caption="Your Uploaded Image", use_container_width=True)
original_image = image.copy()


# Rotation 
st.sidebar.subheader("Image Rotation")
rotation_options = st.sidebar.selectbox("Choose rotation", ["0°", "90°", "180°", "270°"])

if rotation_options == "90°":
    image = image.rotate(-90, expand=True)
elif rotation_options == "180°":
    image = image.rotate(180, expand=True)
elif rotation_options == "270°":
    image = image.rotate(-270, expand=True)
    

# Aspect Ratio
st.sidebar.subheader("Aspect Ratio Crop")

aspect_choice = st.sidebar.selectbox(
    "Choose target aspect ratio:",
    [
        "Original",
        "1:1",
        "4:3",
        "16:9",
        "9:16",
        "3:2",
        "21:9"
    ]
)

if aspect_choice != "Original":
    w_ratio, h_ratio = map(int, aspect_choice.split(':'))
    target_ratio = w_ratio / h_ratio

    img_w, img_h = image.size
    current_ratio = img_w / img_h

    if current_ratio > target_ratio:
        crop_h = img_h
        crop_w = int(crop_h * target_ratio)
        max_x = img_w - crop_w
        max_y = 0
    else:
        crop_w = img_w
        crop_h = int(crop_w / target_ratio)
        max_x = 0
        max_y = img_h - crop_h

    offset_x = st.sidebar.slider("Horizontal offset", 0, max_x, max_x // 2) if max_x > 0 else 0
    offset_y = st.sidebar.slider("Vertical offset", 0, max_y, max_y // 2) if max_y > 0 else 0

    left = offset_x
    top = offset_y
    right = left + crop_w
    bottom = top + crop_h

    cropped = image.crop((left, top, right, bottom))
    image = ImageOps.pad(cropped, (crop_w, crop_h), color=(255, 255, 255))


#Adjusting Brightness and Contrast
st.sidebar.subheader("Adjusting Tools")
brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0, 0.1)
saturation = st.sidebar.slider("Saturation", 0.5, 2.0, 1.0, 0.1)

enhancer = ImageEnhance.Brightness(image)
image = enhancer.enhance(brightness)

enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(contrast)

enhancer = ImageEnhance.Sharpness(image)
image = enhancer.enhance(sharpness)

enhancer = ImageEnhance.Color(image)
image = enhancer.enhance(saturation)

vignette_strength = st.sidebar.slider("Vignette", 0.0, 2.0, 0.0, 0.1)

if vignette_strength > 0:
    import numpy as np
    img_np = np.array(image).astype(np.float32)
    rows, cols = img_np.shape[:2]

    X = np.linspace(-1, 1, cols)
    Y = np.linspace(-1, 1, rows)
    X, Y = np.meshgrid(X, Y)
    radius = np.sqrt(X**2 + Y**2)

    mask = 1 - (radius / radius.max())
    mask = np.clip(mask, 0, 1) ** vignette_strength
    mask = mask[..., np.newaxis] 

    vignette_img = img_np * mask
    vignette_img = np.clip(vignette_img, 0, 255).astype(np.uint8)
    image = Image.fromarray(vignette_img)


# Add Text Section
st.sidebar.subheader("Add Text to Image")
add_text = st.sidebar.checkbox("Add Text")

if add_text:
    user_text = st.sidebar.text_input("Enter text:", "Hello Streamlit!")
    font_size = st.sidebar.slider("Font size", 10, 200, 50)
    text_color = st.sidebar.color_picker("Text color", "#FF0000")

    x_offset = st.sidebar.slider("Horizontal Offset", -1000, 1000, 0)
    y_offset = st.sidebar.slider("Vertical Offset", -1000, 1000, 0)
    stylish_fonts = [
        "Arial", "Verdana", "Tahoma", "Impact", "Courier New", 
        "Georgia", "Comic Sans MS", "Trebuchet MS", "Lucida Console", 
        "Palatino Linotype", "Century Gothic", "Garamond", 
        "Franklin Gothic Medium", "Calibri", "Lucida Sans"
    ]
    font_choice = st.sidebar.selectbox("Choose Font", stylish_fonts)

    try:
        font_path = next(f.fname for f in fm.fontManager.ttflist if f.name == font_choice)
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()  

    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), user_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    img_width, img_height = image.size
    base_x = (img_width - text_width) // 2
    base_y = (img_height - text_height) // 2
    pos_x = max(0, min(base_x + x_offset, img_width - text_width))
    pos_y = max(0, min(base_y + y_offset, img_height - text_height))
    pos = (pos_x, pos_y)

    draw.text(pos, user_text, fill=text_color, font=font)


# Filters
st.sidebar.header("Image Filters")
filter_options = st.sidebar.selectbox(
    "Choose a filter:",
    [
        "None",
        "Invert Colors",
        "Grayscale",
        "Old Film (Sepia)",
        "Outlines",
        "Warm Tone",
        "Cool Tone",
        "Vintage Fade",
        "High Contrast",
        "Soft Pastel"
    ]
)
filter_intensity = st.sidebar.slider("Filter Intensity", 0.0, 2.0, 1.0, 0.1)

# Sky Styles Section
st.sidebar.header("Sky Styles")
sky_options = st.sidebar.selectbox(
    "Choose a sky style:",
    [
        "None",
        "Bright Day",
        "Golden Hour",
        "Sunset Glow",
        "Night Sky",
        "Stormy Mood"
    ]
)

sky_intensity = st.sidebar.slider("Sky Style Intensity", 0.0, 2.0, 1.0, 0.1)

# Processing Logic
img_np = np.array(image).astype(np.float32)
def blend_effect(original, effect, factor):
    blended = original * (1 - factor) + effect * factor
    blended = np.clip(blended, 0, 255)
    return blended.astype(np.uint8)

def apply_color_tint(img, r_mul, g_mul, b_mul):
    tinted = img.astype(np.float32).copy()
    tinted[..., 0] *= r_mul
    tinted[..., 1] *= g_mul
    tinted[..., 2] *= b_mul
    return np.clip(tinted, 0, 255).astype(np.uint8)
# --- Apply Filter ---
effect = img_np.copy()
if filter_options == "Invert Colors":
    effect = 255 - img_np
elif filter_options == "Grayscale":
    gray = img_np.mean(axis=2, keepdims=True)
    effect = np.repeat(gray, 3, axis=2)
elif filter_options == "Old Film (Sepia)":
    r, g, b = img_np[..., 0], img_np[..., 1], img_np[..., 2]
    sepia_r = r * 0.393 + g * 0.769 + b * 0.189
    sepia_g = r * 0.349 + g * 0.686 + b * 0.168
    sepia_b = r * 0.272 + g * 0.534 + b * 0.131
    effect = np.stack([sepia_r, sepia_g, sepia_b], axis=-1)
elif filter_options == "Outlines":
    from PIL import ImageFilter
    effect_img = Image.fromarray(img_np.astype(np.uint8)).filter(ImageFilter.FIND_EDGES)
    effect = np.array(effect_img).astype(np.float32)
elif filter_options == "Warm Tone":
    effect = apply_color_tint(img_np, 1.4, 1.2, 0.9)
elif filter_options == "Cool Tone":
    effect = apply_color_tint(img_np, 0.9, 1.2, 1.4)
elif filter_options == "Vintage Fade":
    effect = img_np * 0.6 + 80
elif filter_options == "High Contrast":
    factor = 2.0
    effect = 128 + factor * (img_np - 128)
elif filter_options == "Soft Pastel":
    effect = img_np * 0.8 + 50

if filter_options != "None":
    img_np = blend_effect(img_np, effect, filter_intensity)

# --- Apply Sky Style ---
sky_effect = img_np.copy()
if sky_options == "Bright Day":
    sky_effect = apply_color_tint(img_np, 1.2, 1.2, 1.3)
elif sky_options == "Golden Hour":
    sky_effect = apply_color_tint(img_np, 1.4, 1.2, 0.9)
elif sky_options == "Sunset Glow":
    sky_effect = apply_color_tint(img_np, 1.5, 1.0, 0.8)
elif sky_options == "Night Sky":
    sky_effect = img_np * 0.5
    sky_effect[..., 2] *= 1.8
elif sky_options == "Stormy Mood":
    sky_effect = img_np * 0.7
    sky_effect[..., 0] *= 0.8
    sky_effect[..., 2] *= 1.4

if sky_options != "None":
    img_np = blend_effect(img_np, sky_effect, sky_intensity)
image = Image.fromarray(img_np.astype(np.uint8))
st.image(image, caption="Edited Image", use_container_width=True)


#RGB
st.sidebar.subheader("Color Channels")
show_channels = st.sidebar.checkbox("Show Color Channels")

if show_channels:
    image_array = np.array(image)
    r, g, b = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]
    
    red_img = np.zeros_like(image_array)
    green_img = np.zeros_like(image_array)
    blue_img = np.zeros_like(image_array)

    red_img[:, :, 0] = r
    green_img[:, :, 1] = g
    blue_img[:, :, 2] = b
    
    st.subheader("Color Channels")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(red_img, caption="Red Channel", use_container_width=True)

    with col2:
        st.image(green_img, caption="Green Channel", use_container_width=True)

    with col3:
        st.image(blue_img, caption="Blue Channel", use_container_width=True)


# Colormapped Image Section
apply_colormap = st.sidebar.checkbox("Show Colormapped Image")
color_map = st.sidebar.selectbox(
    "Select a colormap",
    [
        # perceptually uniform sequential
        "viridis", "plasma", "inferno", "magma", "cividis",
        # sequential
        "Greys", "Purples", "Blues", "Greens", "Oranges", "Reds",
        # sequential (multi-hue)
        "YlOrBr", "YlOrRd", "OrRd", "PuRd", "RdPu",
        "BuPu", "GnBu", "PuBu", "YlGnBu", "PuBuGn", "BuGn", "YlGn",
        # diverging
        "PiYG", "PRGn", "BrBG", "PuOr", "RdGy", "RdBu",
        "RdYlBu", "RdYlGn", "Spectral", "coolwarm",
        # cyclical
        "twilight", "twilight_shifted", "hsv",
        # qualitative
        "Pastel1", "Pastel2", "Paired", "Accent",
        "Dark2", "Set1", "Set2", "Set3",
        # misc
        "hot", "afmhot", "gist_heat", "copper", "cool", "spring", "summer", "autumn", "winter", "bone", "pink", "gray"
    ]
)
if apply_colormap:
    st.subheader("Color Mapped Image")
    gray_image = image.convert("L")
    gray_array = np.array(gray_image)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(gray_array, cmap=color_map)
    ax.axis("off")
    st.pyplot(fig)


# Original Image vs Edited Image
st.subheader("Original Image vs Edited Image")
col1, col2 = st.columns(2)
with col1:
    st.image(original_image, caption="Original Image", use_container_width=True)

with col2:
    st.image(image, caption="Edited Image", use_container_width=True)


# Download Colormaps / Color Channels 
st.sidebar.subheader("Download Options")
# Color Channels Download
if show_channels:
    # st.sidebar.markdown("**Download Color Channels:**")
    for channel_name, channel_img in zip(
        ["Red Channel", "Green Channel", "Blue Channel"], 
        [red_img, green_img, blue_img]
    ):
        buf = BytesIO()
        Image.fromarray(channel_img).save(buf, format="PNG")
        buf.seek(0)
        
        st.sidebar.download_button(
            label=f"Download {channel_name}",
            data=buf,
            file_name=f"{channel_name}.png",
            mime="image/png"
        )

# Colormap Download
if apply_colormap:
    # st.sidebar.markdown("**Download Colormap Image:**")
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    colormap_img = Image.open(buf)
    
    st.sidebar.download_button(
        label=f"Download {color_map} Colormap",
        data=buf,
        file_name=f"{color_map}.png",
        mime="image/png"
    )

# Download button
download_name = st.sidebar.text_input("Enter filename (without extension):", "edited_image")
img_bytes = BytesIO()
image.save(img_bytes, format="JPEG")
img_bytes.seek(0)
st.sidebar.download_button(
    label="Download Edited Image",
    data=img_bytes,
    file_name=f"{download_name}.jpg",
    mime="image/jpeg"
)
