import io
import base64
import logging
import json
import httpx
import pypdfium2 as pdfium
from PIL import Image
from .config import settings
from .schemas import DocumentData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROMPT = """
You are an advanced document intelligence system. Analyze this document image carefully.
This image may contain multiple pages stitched together vertically. Process all sections completely.
Extract all text entries, organization names, dates, amounts, and specific item rows across the entire document layout.

Return your complete final answer strictly as a raw JSON object string matching this key outline blueprint exactly. Do not add markdown backticks, explanations, or chatter:
{
  "document_type": string or null,
  "language": string or null,
  "document_title": string or null,
  "date": string or null,
  "document_number": string or null,
  "person_name": string or null,
  "organization_name": string or null,
  "address": string or null,
  "phone": string or null,
  "email": string or null,
  "subtotal": float or null,
  "tax": float or null,
  "total_amount": float or null,
  "currency": string or null,
  "confidence": float or null,
  "items": [
    {
      "name": string or null,
      "quantity": float or null,
      "unit": string or null,
      "unit_price": float or null,
      "amount": float or null
    }
  ]
}
"""

async def analyze_document(file_path: str):
    logger.info("Encoding source document layout parameters...")
    
    # 1. Handle Multi-page PDFs natively without external system tool dependencies
    if file_path.lower().endswith('.pdf'):
        logger.info("PDF file detected. Stitching all pages vertically into a single image canvas...")
        pdf = pdfium.PdfDocument(file_path)
        pil_images = []
        
        # Render every single page in the PDF into an image array layer
        for page in pdf:
            bitmap = page.render(scale=1.5) # Balance resolution and upload file size cleanly
            pil_img = bitmap.to_pil()
            pil_images.append(pil_img)
            
        if not pil_images:
            raise Exception("Failed to extract pages from the PDF document.")
            
        # Stitch all pages vertically into one long continuous image canvas
        total_width = max(img.width for img in pil_images)
        total_height = sum(img.height for img in pil_images)
        
        combined_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))
        
        current_y = 0
        for img in pil_images:
            combined_image.paste(img, (0, current_y))
            current_y += img.height
            
        image_obj = combined_image
    else:
        # Handle standard images (JPG/PNG) directly
        logger.info("Standard image file detected.")
        image_obj = Image.open(file_path)

    # 2. Compress and convert the compiled image into a base64 string payload
    buffered = io.BytesIO()
    image_obj.save(buffered, format="JPEG", quality=85)
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
    payload = {
        "image": base64_image,
        "prompt": PROMPT
    }
    
    target_url = f"{settings.colab_api_url.rstrip('/')}/analyze_colab"
    logger.info(f"Shipping compiled image payload to cloud GPU bridge: {target_url}")
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(target_url, json=payload)
        
        if response.status_code != 200:
            logger.error(f"Cloud model returned error state: {response.text}")
            raise Exception("Remote cloud infrastructure model inference failure.")
            
        json_response = response.json()
        raw_output = json_response["data"]
        
        if isinstance(raw_output, str):
            start_idx = raw_output.find('{')
            end_idx = raw_output.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                cleaned_json_string = raw_output[start_idx:end_idx]
                parsed_dict = json.loads(cleaned_json_string)
            else:
                raise Exception("Could not isolate valid JSON string structure from cloud payload.")
        else:
            parsed_dict = raw_output

        if "items" not in parsed_dict or not parsed_dict["items"]:
            parsed_dict["items"] = []

        return DocumentData(**parsed_dict)
  