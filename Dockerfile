FROM python:3.12

# fix: https://stackoverflow.com/questions/7446187/no-module-named-pkg-resources
RUN pip install setuptools

RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt --ignore-installed
COPY . /code/
