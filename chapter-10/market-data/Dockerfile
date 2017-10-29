FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-c", "config.py", "service:app"]
EXPOSE 8000
