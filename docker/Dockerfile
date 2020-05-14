FROM continuumio/anaconda3:2020.02
MAINTAINER Nur Lan <nurlan@mail.tau.ac.il>, Anton Melnikov <hello@antonmelnikov.com>
LABEL description="Rule-based Morpho-Phonology Learner. Docker image fixed by Anton Melnikov"

# Ubuntu packages
RUN apt-get update && apt-get install -y build-essential wget libbz2-dev git redis-server

# Install OpenFST
RUN cd /tmp && wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.0.tar.gz && tar xzvf openfst-1.6.0.tar.gz && cd openfst-1.6.0 && ./configure --enable-far --enable-pdt --enable-mpdt && make && make install

# Install virtualenv and Python packages
RUN conda install -c conda-forge -y python=3.6 pyfst pandoc gmpy2 scopy requests plotly boto3 deap redis-py

RUN pip install https://github.com/taucompling/fado-python3.git

CMD python run_genetic_algorithm.py
