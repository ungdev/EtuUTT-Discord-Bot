ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-alpine

# Set server url
ENV SERVER_URL=http://0.0.0.0:3000
# Set workdir and copy needed files
WORKDIR /usr/src/etuutt
COPY . .

# Install requirements
RUN pip --no-cache-dir install -U pip -r requirements.txt

# Default port of the web server
EXPOSE 3000
# Default command
CMD ["python3", "-m", "etuutt_bot"]
