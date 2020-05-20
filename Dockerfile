FROM python:3

ADD FindSecret.py /

RUN pip install pystrich
RUN pip install requests
RUN git clone https://github.com/wolfSSL/wolfssh.git ./wolfssh
CMD [ "python", "./FindSecret.py", "./wolfssh", "rsa_key" ]
