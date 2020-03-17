FROM frolvlad/alpine-python3

WORKDIR /etc/covid
COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "scrape.py"]
