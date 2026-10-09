FROM itsafeaturemythic/mythic_python_go:latest

RUN pip3 install mythic_container==0.5.12

RUN pip3 install pyminizip py7zr pycdlib cabarchive pylnk3 mslex jinja2

RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common

RUN apt-get update && apt-get install -y --no-install-recommends msitools wixl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /Mythic/

CMD ["python3", "main.py"]
