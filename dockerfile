FROM public.ecr.aws/lambda/python:3.13.2025.11.22.14

# Install system dependencies for Pillow
RUN dnf install -y \
    libjpeg-devel \
    zlib-devel \
    libpng-devel \
    && dnf clean all

# Copy requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/

CMD ["lambda_handler.handler"]