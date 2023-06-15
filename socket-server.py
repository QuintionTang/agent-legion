import argparse
import os
import socket
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler

from utils.FlushingFileHandler import FlushingFileHandler

console_logger = logging.getLogger()
console_logger.setLevel(logging.INFO)
FORMAT = '%(asctime)s %(levelname)s %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(FORMAT))
console_logger.setLevel(logging.INFO)
file_handler = FlushingFileHandler(
    "log.log", formatter=logging.Formatter(FORMAT))
file_handler.setFormatter(logging.Formatter(FORMAT))
file_handler.setLevel(logging.INFO)
console_logger.addHandler(file_handler)
console_logger.addHandler(console_handler)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--APIKey", type=str, nargs='?',
                        default=os.getenv("OPENAI_API_KEY"), required=False)
    parser.add_argument("--accessToken", type=str, nargs='?',
                        default=os.getenv("ACCESS_TOKEN", ""), required=False)
    parser.add_argument("--model", type=str, nargs='?',
                        default=os.getenv("MODEL", "gpt-3.5-turbo"), required=False)
    return parser.parse_args()


class Server():
    def __init__(self, args):
        self.addr = None
        self.connection = None
        logging.info('Initializing Socket Server...')
        self.host = "0.0.0.0"
        self.port = 8006
        # Create a TCP/IP socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10240000)
        self.s.bind((self.host, self.port))

    def listen(self):
        # MAIN SERVER LOOP
        while True:
            # Wait for a connection
            print('waiting for a connection')
            self.s.listen()
            logging.info(f"Server is listening on {self.host}:{self.port}...")
            self.connection, self.addr = self.s.accept()
            logging.info(f"Connected by {self.addr}")
            self.connection.sendall(b'%s' %
                                    self.char_name[args.character][2].encode())


if __name__ == '__main__':
    try:
        args = parse_args()
        print(args)
        s = Server(args)
        s.listen()
    except Exception as e:
        logging.error(e.__str__())
        logging.error(traceback.format_exc())
        raise e
