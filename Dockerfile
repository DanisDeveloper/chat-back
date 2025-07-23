FROM python:3.12.8

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv

COPY . .

RUN uv sync

ENTRYPOINT ["uv", "run", "python", "main.py"]