FROM ubuntu:18.04
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
WORKDIR /backend
COPY . /backend
RUN pip install -r requirements.txt
WORKDIR /backend/api
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["api.py"]
