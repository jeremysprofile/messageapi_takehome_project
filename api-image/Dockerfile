FROM python:3.9-buster
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN echo "9f73807c80d14930494021d23abc222c9dd5a1c2731510a2b4d0f835fcc0ae4e mariadb_repo_setup" \
    | sha256sum -c -
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup \
   --mariadb-server-version="mariadb-10.5" --skip-check-installed
RUN apt install -y mariadb-client
RUN apt update && apt upgrade -y
RUN pip3 install poetry
RUN python -m venv /venv
EXPOSE 5000
COPY ./api ./api
# yes, this should just be 'install the package from PyPI', but I didn't want to upload a take-home project to PyPI
RUN . /venv/bin/activate && cd ./api && poetry install
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
