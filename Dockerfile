# Knowledge system web app. Retrieval, the library, flashcards and maps run as-is.
# Anything that calls Claude (Ask answers, digest, tutor) needs the `claude` CLI signed in inside the container;
# the image does not ship credentials.
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
# fastembed (ONNX, no PyTorch) enables semantic search; the app falls back to keyword search without it
RUN pip install --no-cache-dir -r requirements.txt fastembed numpy

COPY app ./app
COPY tools ./tools
COPY docs ./docs
COPY kb web ./

# Bind to all interfaces INSIDE the container; compose publishes the port on 127.0.0.1 only
ENV KB_HOST=0.0.0.0 KB_PORT=8765 PYTHONUNBUFFERED=1
EXPOSE 8765
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request as u; u.urlopen(u.Request('http://127.0.0.1:8765/api/health', headers={'Host':'127.0.0.1:8765'}))"
CMD ["python", "-m", "app.server"]
