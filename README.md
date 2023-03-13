# PGrab

PGrab is a banner grabber tool used to gather information about a remote server or device, specifically the banner or header information that is sent when a connection is made.

## Installation Through PIP
To install dependencies, use the following command:

```bash
pip3 install -r requirements.txt
```

## Installation with Docker
This tool can also be used with [Docker](https://www.docker.com/). To set up the Docker environment, follow these steps (trying using with sudo, if you get any error):

```bash
docker build -t pgrab:latest .
```

# Using the PGrab
To run the PGrab on a domain or IP, provide the domain/IP as an argument with the flag -p to give port number:
```bash
python main.py example.com -p 80 --path /
```

For an overview of all commands use the following command:

```bash
python3 pgrab.py -h
```

The output shown below are the latest supported commands.

```bash
usage: python main.py [-h] -p PORT [--path PATH] [-o file_path] [-v] ip/hostname

PGrab is a banner grabber tool used to gather information about a remote server or device.

positional arguments:
  ip/hostname           IP address or hostname

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port number
  --path PATH           Path to request
  -o file_path, --output file_path
                        Output file name
  -v, --version         show program's version number and exit

Example: python3 main.py 198.168.0.1 -p 22 --path /
```

## Using the Docker Container

A typical run through Docker would look as follows:

```bash
docker run -it --rm pgrab example.com -p 80 --path /
```

**NOTE:** Banner grabbing can be used for legitimate purposes, such as network auditing and security testing, but can also be used for malicious purposes, so use this script responsibly and with permission from the target owner.

**TODO:**
  * Add support for other protocols such as:
    * https (443)
    * dns (53)
    * many more...