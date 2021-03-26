FROM 432228403865.dkr.ecr.eu-central-1.amazonaws.com/conda-base:latest
SHELL [ "/bin/bash", "--login", "-c" ]

COPY environment.yml requirements.txt /tmp/

COPY postBuild.sh /usr/local/bin/postBuild.sh
RUN chmod u+x /usr/local/bin/postBuild.sh
COPY docker/entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh

COPY app /usr/local/bin/app
COPY app/nginx.conf /etc/nginx

RUN chmod u+x /usr/local/bin/app/start.sh


RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile

RUN conda init bash
ENV PROJECT_DIR $HOME/app
WORKDIR $PROJECT_DIR
ENV ENV_PREFIX $PWD/env

# RUN conda update --name base --channel defaults conda && \
#     conda env create --prefix $ENV_PREFIX --file /tmp/environment.yml --force && \
#     conda clean --all --yes

WORKDIR /usr/local/bin/app/



RUN conda activate $ENV_PREFIX && \
    /usr/local/bin/postBuild.sh && \
    conda deactivate

EXPOSE 80
EXPOSE 8080
EXPOSE 5000

CMD ["./start.sh"]
