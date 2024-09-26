FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY data/data_cleaned.csv data/data_cleaned.csv

COPY requirements.txt .
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

COPY tek_buddy tek_buddy/.

EXPOSE 5000
#CMD ["streamlit", "run", "app.py"]
CMD ["python", "tek_buddy/app.py"]

