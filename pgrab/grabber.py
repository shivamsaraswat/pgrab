import re
import json
import socket

def parse_banner(banner, port) -> dict:
    """
    Parses the banner and returns a dictionary with the status line, headers and body

    :param banner: The banner to parse
    :type banner: str
    :return: A dictionary with the status line, headers and body
    :rtype: dict
    """

    if port == 80:
        banner = banner.split("\r\n")

        item_to_match = ""
        final_data = dict()

        try:
            index_of_item = banner.index(item_to_match)
            status_line = banner[0]
            headers = banner[1:index_of_item]
            body = banner[index_of_item+1:]

            final_data = {
                "status_line": status_line,
                "headers": headers,
                "body": body
            }

        except ValueError:
            final_data = banner

    elif port == 22:
        final_data = banner

    return final_data

def status_code(code) -> str:
    """
    Returns the status of the response code

    :param code: The response code
    :type code: str
    :return: The status of the response code
    :rtype: str
    """
    if code == "200":
        status = "success"
    elif code >= "300" and code < "400":
        status = "redirect"
    elif code >= "400":
        status = "error"

    return status

def grabber(domain, port, path="/") -> str:
    """
    Grabs the banner from the target IP and port

    :param ip: The IP address or hostname
    :type ip: str
    :param port: The port number
    :type port: int
    :param path: The path
    :type path: str
    :return: A JSON string with the banner
    :rtype: str
    """

    banner = str()
    banner_dict = dict()
    status = str()

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a timeout of 5 seconds
    s.settimeout(5)

    # pattern to match domain address
    pattern = r'\b[A-Za-z0-9]+\.[A-Z|a-z]{2,}\b'

    if re.match(pattern, domain):
        banner_dict = {
            'domain': domain,
        }
    else:
        banner_dict = {
            'ip': domain,
        }

    try:
        # Get the service name from the port number
        service = socket.getservbyport(port)

        # Create the request
        request = f"GET {path} HTTP/1.1\r\nHost: {domain}\r\n\r\n"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((domain, port))
            s.sendall(request.encode())
            banner = s.recv(1024)

        # Get the response code of the http request
        response_code = banner.decode().split()[1]

        if service == "http":
            status = status_code(response_code)
        elif service == "ssh":
            status = "success"

        banner_dict.update({
            'data': {
                service: {
                    'status': status,
                    'protocol': service,
                    'result': {
                        'response': parse_banner(banner.decode().strip(), port),
                    }
                }
            }
        })

    except Exception as e:
        banner_dict.update({
            'data': {
                service: {
                    'status': 'error',
                    'protocol': service,
                    'result': {
                        'error': str(e),
                    }
                }
            }
        })

    finally:
        s.close()

    return json.dumps(banner_dict)

