# Use a lightweight Jupyter notebook image
FROM quay.io/jupyter/minimal-notebook:latest

# Switch to root to install system packages
USER root

# Install Python libraries for Data Science and Web
# We include openpyxl for Excel support and fastAPI dependencies for the later web part
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    polars \
    matplotlib \
    seaborn \
    openpyxl \
    fastapi \
    uvicorn \
    python-multipart

# Switch back to the standard user to avoid permission issues
USER ${NB_UID}
