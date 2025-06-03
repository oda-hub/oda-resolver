FROM python:3.13-alpine

ENV POLAR_GRB_DATA_CSV=/data/polar/polar_grbs.csv 

ADD . /build/tnr
RUN mv /build/tnr/data /data

RUN cd /build/tnr && \
    { if [[ -f requirements.txt ]]; then pip install -r requirements.txt; fi; } && \
    pip install . && pip install gunicorn && \
    rm -rf /build/tnr

USER 405

CMD ["gunicorn", "-w", "2", "-t", "300", "--bind", "0.0.0.0:5000", "tnr.service:app"]
