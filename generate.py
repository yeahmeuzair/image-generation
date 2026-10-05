import os
import requests
import io
from PIL import Image

# 1. Grab the title and your new Hugging Face API key
title = os.environ.get("IMAGE_TITLE", "default_image")
api_key = os.environ.get("API_KEY")

# 2. Setup Hugging Face API (Using Stable Diffusion XL)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {api_key}"}

# 3. Apply your strict, hardcoded guidelines
strict_prompt = f'Create a photorealistic, highly detailed editorial news photograph representing the concept of: "{title}". Professional news media aesthetic, cinematic lighting, shallow depth of field, 8k resolution, shot on 35mm lens. STRICT CONSTRAINTS: No animated characters, no cartoons, no illustrations, no 3D renders, no vector art. Photorealistic photography only.'

print(f"Telling Stable Diffusion to generate: {title}...")

# 4. Ask Hugging Face to generate the image
response = requests.post(API_URL, headers=headers, json={"inputs": strict_prompt})

if response.status_code == 200:
    # 5. Extract the generated image data
    img = Image.open(io.BytesIO(response.content))

    # 6. Format the title for a safe file name (removes spaces)
    safe_title = title.replace(" ", "_").lower()
    filename = f"{safe_title}.webp"

    # 7. Compress and Convert to WebP
    print("Converting to WebP and compressing...")
    img.save(filename, "webp", quality=80)
    print(f"Success! Saved as {filename}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
