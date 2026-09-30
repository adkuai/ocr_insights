# Multilingual Hybrid Document Intelligence System
### Powered by FastAPI & Open-Source Qwen2-VL (Hosted via Google Colab GPU)

A high-performance, privacy-conscious micro-utility web application designed to extract structured information from printed or handwritten documents (Images and Multi-Page PDFs). The architecture seamlessly processes complex mixed scripts (English + Hindi Devanagari) and maps unstructured layouts into pristine data grids.

By leveraging a hybrid serverless execution tunnel, this system completely bypasses local hardware constraints (like 8GB RAM or lack of a dedicated GPU) and eliminates big-tech commercial cloud vendor lock-in.

---

## 🚀 Key Architectural Features

*   **Open-Source Core Model:** Driven by the leading open-source Vision-Language Model (`Qwen2-VL`) hosted on a remote cloud GPU, ensuring deep multilingual token reasoning.
*   **Mixed-Script Cursive OCR:** Natively decodes handwritten Hindi text in Devanagari script side-by-side with English characters.
*   **Zero Local Hardware Strain:** The heavy AI inference matrix calculations run entirely inside a cloud GPU. Your local laptop operates purely as a lightweight control dashboard (consuming <150MB of RAM).
*   **Secure Reverse Tunneling:** Utilizes `ngrok` secure port forwarding to create a private network bridge between the local machine and the cloud server.
*   **Multi-Page Stream Parsing:** Employs a robust page-by-page streaming architecture powered by `pypdfium2` to handle massive multi-page corporate PDFs without hitting tunnel bandwidth caps or timing out.
*   **Polished Responsive UI:** Built with custom modern CSS metrics to deliver a lightweight dashboard optimized for desktop, tablet, and mobile viewports.

---

## 🛠️ System Stack & Architecture

```text
 [ Multi-Page PDF / Image ] 
            │
            ▼
    Local FastAPI Server ───(Slices Pages / Formats base64)
            │
            ▼  [ Secure ngrok Tunnel Bridge ]
   Google Colab Cloud GPU (NVIDIA T4 16GB VRAM)
   (Runs Qwen2-VL-2B-Instruct on active background thread)
            │
            ▼  [ Parses Layout Rows into clean JSON ]
    Local FastAPI Server ───(Validates Strict Pydantic Schema)
            │
            ▼
 [ Polished Responsive UI Tables ]
```

*   **Backend Framework:** FastAPI (Python 3.14 Environment compatible)
*   **Local PDF Processing Core:** pypdfium2 / Pillow
*   **Cloud AI Engine:** Hugging Face Transformers / Accelerate / PyTorch / Uvicorn
*   **Tunneling Engine:** Pyngrok (Secure Port Forwarding)
*   **Frontend UI:** Vanilla HTML5 / Custom Mobile-First CSS3 / JavaScript (ES6)

---

## 📂 Project Directory Structure

```text
ocr_insights/                      <-- Main Project Root Folder
│
├── app/
│   ├── config.py                  # Environment configuration & URL handlers
│   ├── collab_services.py         # Handles local page serialization & tunnel streaming
│   ├── main.py                    # Core FastAPI router & validation middleware
│   └── schemas.py                 # Strict Pydantic response data validation contract
│
├── static/
│   ├── index.html                 # Minimalist dashboard markup with embedded spinner
│   └── script.js                  # Asynchronous request mounter & table text injector
│
├── uploads/                       # Temporary system disk cache for processing files
├── .env                           # Stores dynamic ngrok tunnel address
├── .gitignore                     # Prevents system caches and tokens from leaking to GitHub
├── requirements.txt               # Unified project python dependency mapping file
└── README.md                      # Comprehensive system operations manual
```

---

## 💻 Local Setup & Execution Manual

### 1. Initialize the Cloud GPU Server (Google Colab)
1. Open your browser and create a new notebook on **Google Colab**.
2. Go to `Runtime ➔ Change runtime type`, select **T4 GPU**, and save.
3. Paste and run your notebook code server cell.
4. Copy the generated public URL string from the output (e.g., `https://ngrok-free.dev`).

### 2. Configure Local Environment Variables
Create a `.env` file directly inside your root project directory on your laptop:
```env
COLAB_API_URL=https://ngrok-free.dev
```

### 3. Initialize Local Virtual Workspace Environment
Open your VS Code terminal and isolate your workspace packages:
```powershell
# Initialize local sandbox
python -m venv .venv --without-pip
.venv\Scripts\activate

# Install requirements text bundle
python -m ensurepip --default-pip
pip install -r requirements.txt
```

### 4. Boot Up the Local Application Server
```bash
uvicorn app.main:app --reload
```
Navigate your browser tab to `http://127.0.0.1:8000` to interact with your system.
