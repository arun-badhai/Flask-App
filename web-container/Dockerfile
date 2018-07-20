FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# RUN spacy download en_core_web_sm
# or you can install the downloaded file via pip
RUN pip install ./en_core_web_sm-2.0.0.tar.gz
CMD ["python", "app.py"]
