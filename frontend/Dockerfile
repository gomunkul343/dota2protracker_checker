FROM python:latest

EXPOSE 5000
EXPOSE 5900

COPY ./req.txt /tmp/req.txt
COPY . .
RUN pip install --no-cache-dir -r req.txt
WORKDIR /app/
CMD [ "python", "./app.py" ]
