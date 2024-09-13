FROM python:3.11-buster

ARG TARGETARCH=amd64

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE lunch_service.settings

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates bash curl uuid-runtime tree grep bash-completion patool && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
# Install Gunicorn
RUN pip install gunicorn

EXPOSE 8000
COPY . /app

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "lunch_service.wsgi:application", "--bind", "0.0.0.0:8000"]