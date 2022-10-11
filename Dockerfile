FROM continuumio/miniconda3

COPY requirements.txt /tmp/
COPY ./app /app
COPY ./data /data
WORKDIR "/app"

RUN conda install --file /tmp/requirements.txt -c conda-forge -c r -c bioconda

ENTRYPOINT [ "python3" ]
CMD [ "dash_app.py" ]
