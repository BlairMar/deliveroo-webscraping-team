FROM postgres
ENV POSTGRES_PASSWORD ahj%ZF2*TIZk
ENV POSTGRES_USER del
ENV POSTGRES_DB postgresdb

COPY ./init.sql /docker-entrypoint-initdb.d