import os
import subprocess

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

# Allow the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/convert")
async def convert_md_to_pdf(file: UploadFile = File(...)):
    # 1. Save the uploaded markdown file
    input_filename = "input.md"
    output_filename = "output.pdf"

    with open(input_filename, "wb") as f:
        f.write(await file.read())

    # 2. Run Pandoc command inside the container
    # pandoc input.md -o output.pdf
    try:
        subprocess.run(
            ["pandoc", "--pdf-engine=lualatex", input_filename, "-o", output_filename],
            check=True,
        )
    except subprocess.CalledProcessError:
        return {"error": "Conversion failed"}

    # 3. Return the generated PDF
    return FileResponse(
        output_filename, filename="converted.pdf", media_type="application/pdf"
    )
