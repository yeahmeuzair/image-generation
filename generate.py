import os
import io
from PIL import Image
from google import genai
from google.genai import types

# 1. Grab the title and your secret Gemini API key
title = os.environ.get("IMAGE_TITLE", "default_image")
api_key = os.environ.get("API_KEY")

# 2. Connect to the Gemini API
client = genai.Client(api_key=api_key)

# 3. Apply your strict, hardcoded guidelines
strict_prompt = f'Create a photorealistic, highly detailed editorial news photograph representing the concept of: "{title}". Professional news media aesthetic, cinematic lighting, shallow depth of field, 8k resolution, shot on 35mm lens. STRICT CONSTRAINTS: No animated characters, no cartoons, no illustrations, no 3D renders, no vector art. Photorealistic photography only.'

print(f"Telling Gemini to generate: {title}...")

# 4. Ask Gemini to generate the image
response = client.models.generate_content(
    model='gemini-3.1-flash-image',
    contents=strict_prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
        ),
    ),
)

# 5. Extract the generated image data
generated_image_bytes = response.parts[0].inline_data.data
img = Image.open(io.BytesIO(generated_image_bytes))

# 6. Format the title for a safe file name (removes spaces)
safe_title = title.replace(" ", "_").lower()
filename = f"{safe_title}.webp"

# 7. Compress and Convert to WebP (quality=80 applies the compression)
print("Converting to WebP and compressing...")
img.save(filename, "webp", quality=80)

print(f"Success! Saved as {filename}")
