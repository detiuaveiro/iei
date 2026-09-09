FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install build tools, TeX Live, and font packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    texlive-luatex \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    fonts-lmodern \
    fonts-noto \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-dejavu \
    curl \
    unzip \
    ca-certificates \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# 2. Download and install Pandoc (>= 3.1.12 required for mainfontfallback support)
ARG PANDOC_VERSION=3.11
RUN ARCH=$(dpkg --print-architecture) \
    && curl -fLo /tmp/pandoc.tar.gz "https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-linux-${ARCH}.tar.gz" \
    && tar -xzf /tmp/pandoc.tar.gz --strip-components 1 -C /usr/local/ \
    && rm /tmp/pandoc.tar.gz

# 3. Download and install FiraCode Nerd Font
RUN mkdir -p /usr/share/fonts/truetype/firacode \
    && curl -fLo /tmp/FiraCode.zip https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.zip \
    && unzip -q /tmp/FiraCode.zip -d /usr/share/fonts/truetype/firacode \
    && rm /tmp/FiraCode.zip \
    && fc-cache -fv

WORKDIR /data

