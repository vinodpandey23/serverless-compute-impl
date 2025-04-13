FROM python:3.11-slim

WORKDIR /app
RUN pip install virtualenv && python -m virtualenv --always-copy /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY runner.py .
CMD ["python", "-u", "runner.py"]