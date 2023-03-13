import sys
import time
import logging
import argparse
import colorlog
from pgrab import grabber

def parse_arguments() -> argparse.Namespace:
    """
    Parses the arguments passed to the script

    :return: The arguments
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(prog="python main.py", description="PGrab is a banner grabber tool used to gather information about a remote server or device.", epilog="Example: python3 main.py 198.168.0.1 -p 22 --path /")
    parser.add_argument("ip/hostname", help="IP address or hostname")
    parser.add_argument("-p", "--port", required=True,help="Port number")
    parser.add_argument("--path", help="Path to request")
    parser.add_argument("-o", "--output", type=argparse.FileType('w'), metavar='file_path', action='store', dest='output', help="Output file name")
    parser.add_argument("-v", "--version", action="version", version="0.1")
    args = parser.parse_args()

    return args

def main() -> None:

    args = parse_arguments()
    ip_or_hostname = args.__dict__["ip/hostname"]
    port = int(args.port)
    path = args.path
    out = args.output

    if port != 80 and port != 22:
        print("Invalid port number!")
        print("Currently, supported port numbers are 22 and 80.")
        sys.exit(1)

    # Set up the logging system with a ColorFormatter
    handler = logging.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s%(reset)s %(message)s'))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    # start time
    logging.info("started grab at " + time.ctime())

    # grab the banner
    output = grabber.grabber(ip_or_hostname, port, path)

    # write to file
    if out:
        with open(out.name, "w") as f:
            f.write(output)

    print(output)

    # end time
    logging.info("finished grab at " + time.ctime())

if __name__ == "__main__":
    main()