# NanoBanana ComfyUI Node

A custom **ComfyUI** node that integrates Google Gemini API for multimodal image + text generation. It can take image inputs and a text prompt, send them to Gemini, and return either a generated image or text output.

---

## 🌟 Features

- Supports both **environment variable** and **manual input** for API key.
- Converts ComfyUI images to base64 automatically.
- Calls **Gemini 2.5 Flash (Image Preview)** model for multimodal generation.
- Automatically saves output image or text to `output_YYYYMMDD` folder.
- Compatible with multiple image inputs.

---

## 🧩 Installation

1. Navigate to your ComfyUI installation folder.
2. Go to the `custom_nodes` directory:

   ```bash
   cd ComfyUI/custom_nodes
   ```

3. Create a new folder for this node:

   ```bash
   mkdir comfyui-nano-banana-node
   cd comfyui-nano-banana-node
   ```

4. Save the node file as `nano_banana_node.py` inside this folder.
5. Add the following `requirements.txt` file (see below).
6. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

7. Restart ComfyUI. You should now see a new category named **NanoBanana** in the node menu.

---

## ⚙️ Environment Setup

### Option 1: Environment Variable (recommended)

Add your Gemini API key to environment variables:

**Linux / macOS:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Windows PowerShell:**
```powershell
setx GEMINI_API_KEY "your_api_key_here"
```

### Option 2: Node Input
You can also input the API key directly in the node’s `api_key` text box.

---

## 🧠 Usage

- Connect **IMAGE** and **STRING (prompt)** inputs to this node.
- Optionally input your API key (leave blank to use the environment variable).
- When executed, the node will:
  1. Convert images to base64.
  2. Send them with your prompt to Gemini API.
  3. Save and return the generated image or text file.

### Outputs
| Output | Type | Description |
|---------|------|-------------|
| 1 | IMAGE | Generated image from Gemini API |
| 2 | STRING | File path of saved image/text |

---

## 🧾 requirements.txt
```text
Pillow
google-generativeai>=0.5.2
```

---

## 🧰 Troubleshooting

- **`Gemini API key not provided`** → Check environment variable or node input.
- **`Gemini API did not return image or text`** → Try a simpler prompt or ensure model supports image output.
- **`Failed to parse response`** → Inspect ComfyUI console logs for Gemini API raw response.

---

## 🧑‍💻 Author
**NanoBanana ComfyUI Node** — developed for easy Gemini integration with ComfyUI.

Version: 0.1.0  
License: MIT
