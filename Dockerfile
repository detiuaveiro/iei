FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install build tools, pandoc, TeX Live, and font packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    pandoc \
    texlive-luatex \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    fonts-lmodern \
    fonts-noto \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    curl \
    unzip \
    ca-certificates \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# 2. Download and install FiraCode Nerd Font
RUN mkdir -p /usr/share/fonts/truetype/firacode \
    && curl -fLo /tmp/FiraCode.zip https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.zip \
    && unzip -q /tmp/FiraCode.zip -d /usr/share/fonts/truetype/firacode \
    && rm /tmp/FiraCode.zip \
    && fc-cache -fv

WORKDIR /data
