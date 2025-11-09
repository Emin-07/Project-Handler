FROM python:3.13.8-trixie

ENV PYHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .

RUN uv sync

COPY . .

EXPOSE 8000

RUN chmod +x prestart.sh

ENTRYPOINT [ "/app/prestart.sh" ]

CMD ["uv", "run", "python", "main.py"]