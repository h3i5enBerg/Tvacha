import io

import torch
from PIL import Image, ImageOps, UnidentifiedImageError
from torchvision import transforms

MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10 MB

_LESION_TRANSFORM = transforms.Compose(
    [
        transforms.Resize(224, interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


def validate_and_load_image(file_bytes: bytes) -> Image.Image:
    """Validate uploaded image bytes and return an EXIF-corrected RGB PIL Image."""
    if not file_bytes:
        raise ValueError("Uploaded image file is empty.")
    if len(file_bytes) >= MAX_IMAGE_BYTES:
        raise ValueError("Uploaded image exceeds the 10 MB size limit.")

    try:
        with Image.open(io.BytesIO(file_bytes)) as img:
            img.load()
            transposed = ImageOps.exif_transpose(img)
            return transposed.convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError("Invalid or corrupt image file.") from exc


def preprocess_lesion_image(image: Image.Image) -> torch.Tensor:
    """Resize/center-crop to 224x224 and apply ImageNet normalization."""
    rgb_image = image.convert("RGB") if image.mode != "RGB" else image
    tensor = _LESION_TRANSFORM(rgb_image)
    return tensor.unsqueeze(0)
