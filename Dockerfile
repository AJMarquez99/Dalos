FROM --platform=$BUILDPLATFORM python:3.11-alpine AS builder
EXPOSE 8000

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

FROM builder as dev-envs
RUN apk update
RUN apk add git

RUN addgroup -S docker
RUN adduser -S --shell /bin/bash --ingroup docker vscode

# Running Migrations
RUN python manage.py migrate --run-syncdb

RUN python manage.py makemigrations
RUN python manage.py migrate

# Generate API
RUN python manage.py generate-api -f

# Run Dev Server
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
