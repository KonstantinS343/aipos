from server import HTTPServer
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S',
)


if __name__ == '__main__':
    serv = HTTPServer()

    try:
        serv.run()
    except KeyboardInterrupt:
        pass
