FROM python:3.8

ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

ADD magic-backend /magic-backend
RUN (cd /magic-backend; pip install -r requirements.txt; pip install .)

ENV API_BASE=/staging-1-3/magic

# advantage of calling gunicorn like that instead of from python is that the parameters are more explicit
# 8 cpu is requested for the container and can be set as variable

ENV HOME=/tmp/home

ENTRYPOINT mkdir -pv $HOME; run_magic_back_end.py -conf_file /conf/magic_data_server/config.yml
#ENTRYPOINT mkdir -pv $HOME; gunicorn --timeout 60 --workers 8 magic_data_server.backend_api:micro_service -b 0.0.0.0:8000 --log-level DEBUG 
