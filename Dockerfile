FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV UWSGI_INI /flashinger/uwsgi.ini
ENV STATIC_PATH /flashinger/uimgmt/static
ENV LISTEN_PORT 8089

EXPOSE 8089

COPY ./requirements.txt /requirements.txt 
RUN pip install -r /requirements.txt 

COPY ./flashinger /flashinger

WORKDIR /flashinger
