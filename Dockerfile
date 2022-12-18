FROM python:3.8

COPY requirements.txt ./requirements.txt

RUN python -m pip install -U pip && \
    python -m pip install -r requirements.txt && \
    python -m pip cache purge

COPY ./ /app/

WORKDIR /app/

CMD uvicorn src.api_run:app --h11-max-incomplete-event-size 100000000 --host=0.0.0.0 --port=${PORT:-5011}