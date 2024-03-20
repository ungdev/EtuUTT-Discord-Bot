ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-alpine

# Set workdir and copy needed files
WORKDIR /usr/src/etuutt
COPY . .

# Update pip and install requirements
RUN pip install -U pip \
    && pip install -r requirements.txt

# Port of the web server
EXPOSE 3000
# Default command
CMD ["python", "-m", "etuutt_bot"]
