FROM python:3.12-trixie

# 1. Install system dependencies
RUN apt update && apt install -y \
    texlive-luatex texlive-latex-recommended \
    texlive-latex-extra texlive-fonts-recommended \
    texlive-fonts-extra fonts-lmodern fonts-noto \
    fonts-noto-cjk fonts-noto-color-emoji pandoc \
    curl unzip fontconfig \
    && rm -rf /var/lib/apt/lists/*

# 2. Download and Install FiraCode Nerd Font
RUN mkdir -p /usr/share/fonts/truetype/firacode \
    && curl -fLo /tmp/FiraCode.zip https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.zip \
    && unzip /tmp/FiraCode.zip -d /usr/share/fonts/truetype/firacode \
    && rm /tmp/FiraCode.zip \
    && fc-cache -fv

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
