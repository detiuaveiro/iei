FROM python:3.12-trixie

# Install system dependencies (Pandoc and LaTeX)
RUN apt update && apt install -y \
    texlive-luatex texlive-latex-recommended \
    texlive-latex-extra texlive-fonts-recommended \
    texlive-fonts-extra fonts-lmodern fonts-noto \
    fonts-noto-cjk fonts-noto-color-emoji pandoc\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
