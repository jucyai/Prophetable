FROM python:3.7

RUN pip install --upgrade setuptools
RUN pip install cython
RUN pip install numpy
RUN pip install pandas
RUN pip install matplotlib
RUN pip install pystan
RUN pip install fbprophet
RUN pip install redis

RUN mkdir -p /home/project/job
WORKDIR /home/project/job
COPY . /home/project/job

ENTRYPOINT [ "python", "app/run.py" ]