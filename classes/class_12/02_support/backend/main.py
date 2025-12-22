import os
import subprocess
import tempfile
import uuid

from fastapi import FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/convert")
async def convert_md_to_pdf(file: UploadFile = File(...)):
    # 1. Generate a unique ID for this request
    unique_id = str(uuid.uuid4())

    # Get the system's temporary directory
    temp_dir = tempfile.gettempdir()

    # Create unique file paths using the UUID
    input_filename = f"{unique_id}.md"
    output_filename = f"{unique_id}.pdf"

    input_path = os.path.join(temp_dir, input_filename)
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # 2. Save uploaded file
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # 3. Run Pandoc
        subprocess.run(
            ["pandoc", "--pdf-engine=lualatex", input_path, "-o", output_path],
            check=True,
            capture_output=True,
        )

        # 4. Read the generated PDF into memory
        with open(output_path, "rb") as f:
            pdf_content = f.read()

        # 5. CLEANUP: Delete files immediately
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

        # 6. Return the raw bytes
        # We set "Content-Disposition" so the browser treats it as a file download
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=converted.pdf"},
        )

    except subprocess.CalledProcessError as e:
        # Cleanup input if it exists
        if os.path.exists(input_path):
            os.remove(input_path)
        return {"error": "Conversion failed", "details": e.stderr.decode()}

    except Exception as e:
        # Cleanup anything left behind
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        return {"error": str(e)}
