import os
import folder_paths
import time
from PIL import Image
from io import BytesIO
import base64
import google.generativeai as genai

class NanoBananaAPINode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True}),
                "api_key": ("STRING", {"default": "", "multiline": False, "placeholder": "Leave empty to use GEMINI_API_KEY env var"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "process"
    CATEGORY = "NanoBanana"

    def __init__(self):
        pass

    def process(self, images, prompt, api_key):
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        key = api_key.strip() or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("Gemini API key not provided (set GEMINI_API_KEY or input in the node)")

        # Configure Gemini client
        genai.configure(api_key=key)
        client = genai

        # Convert ComfyUI images to PIL
        pil_images = []
        for img in images:
            if isinstance(img, Image.Image):
                pil_images.append(img)
            else:
                pil_images.append(Image.fromarray(img))

        # Encode images as Gemini API-compatible parts
        image_parts = []
        for pil_img in pil_images:
            buffer = BytesIO()
            pil_img.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            image_parts.append({"mime_type": "image/png", "data": base64.b64encode(image_bytes).decode("utf-8")})

        # Combine prompt + images into contents
        contents = image_parts + [prompt]

        # Call Gemini API
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-image-preview",
                contents=contents,
            )
        except Exception as e:
            raise RuntimeError(f"Gemini API request failed: {e}")

        # Extract image from Gemini response
        output_image = None
        try:
            if hasattr(response, 'image') and response.image:
                output_image = Image.open(BytesIO(response.image))
            elif hasattr(response, 'parts'):
                for part in response.parts:
                    if part.mime_type.startswith('image/'):
                        data = base64.b64decode(part.data)
                        output_image = Image.open(BytesIO(data))
                        break
            elif hasattr(response, 'text'):
                # If only text output (no image)
                text_result = response.text
                output_dir = os.path.join(folder_paths.get_output_directory(), f"output_{time.strftime('%Y%m%d')}")
                os.makedirs(output_dir, exist_ok=True)
                filename = f"text_{time.strftime('%Y_%m_%d-%H_%M_%S')}.txt"
                file_path = os.path.join(output_dir, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_result)
                return (None, file_path)

        except Exception as e:
            raise RuntimeError(f"Failed to parse Gemini API response: {e}")

        if output_image is None:
            raise ValueError("Gemini API did not return an image or text output.")

        # Save output image
        output_dir = os.path.join(folder_paths.get_output_directory(), f"output_{time.strftime('%Y%m%d')}")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"nano_banana_{time.strftime('%Y_%m_%d-%H_%M_%S')}.png"
        output_path = os.path.join(output_dir, filename)
        output_image.save(output_path, "PNG")

        return (output_image, output_path)
