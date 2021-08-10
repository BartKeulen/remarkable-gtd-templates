FROM python:3.9-slim-buster
WORKDIR /gtd
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install \
  librsvg2-bin \
  make \
  pdf2svg \
  poppler-utils \
  texlive-fonts-extra \
  texlive-fonts-recommended \
  texlive-generic-recommended \
  texlive-latex-base \
  texlive-latex-recommended
RUN apt-get clean
COPY * ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD make
