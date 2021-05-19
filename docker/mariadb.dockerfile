FROM library/mariadb:10.5
MAINTAINER Wilson Assis

RUN touch /var/run/mysqld/mysqld.sock
RUN touch /var/run/mysqld/mysqld.pid
RUN chown -R mysql:mysql /var/run/mysqld/mysqld.sock
RUN chown -R mysql:mysql /var/run/mysqld/mysqld.pid
RUN chmod -R 644 /var/run/mysqld/mysqld.sock
RUN chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

EXPOSE 3306