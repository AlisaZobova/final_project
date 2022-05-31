FROM python:3.8-slim-buster

WORKDIR /final_project

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN chmod u+x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
