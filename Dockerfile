FROM python:3.9-slim-bullseye AS build
COPY requirements.txt .
RUN pip install -r ./requirements.txt

FROM gcr.io/distroless/python3
LABEL authors="mrpmuzyka@gmail.com"
COPY --from=build /usr/local/lib/python3.9/site-packages/ /usr/lib/python3.9/.
COPY . /app
WORKDIR /app
USER 65532
CMD ["main.py"]
