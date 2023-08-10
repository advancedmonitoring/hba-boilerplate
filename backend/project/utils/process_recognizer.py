import argparse
import sys

from django.utils.functional import classproperty


class ProcessRecognizer:
    __initialized: bool = False
    __name: str = None
    __queue: str = None
    __run_command: str = None
    __management_command: str = None

    @classproperty
    def process_name(cls):
        return cls.__name

    @classproperty
    def command(cls):
        return cls.__run_command

    @classproperty
    def management_command(cls):
        return cls.__management_command

    @classproperty
    def queue(cls):
        return cls.__queue

    @classmethod
    def init(cls):
        if cls.__initialized:
            return

        cls.__run_command = ' '.join(sys.argv)
        *_, cls.__name = sys.argv[0].rpartition('/')

        cls.__initialized = True

        if cls.is_celery():
            cls.__set_queue()

        if cls.is_management():
            cls.__set_management_command()

    @classmethod
    def is_management(cls):
        return 'manage.py' in cls.__run_command

    @classmethod
    def is_celery(cls):
        return 'celery' in cls.__run_command

    @classmethod
    def is_celery_worker(cls):
        return cls.is_celery() and 'worker' in cls.__run_command

    @classmethod
    def is_server(cls):
        if not cls.is_management():
            return cls.__name in {'daphne', 'gunicorn'}

        return 'runserver' in cls.__run_command or 'runworker' in cls.__run_command

    @classmethod
    def __set_queue(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('-Q', '--queues', default="default")
        args, _ = parser.parse_known_args()
        cls.__queue = args.queues

    @classmethod
    def __set_management_command(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('command')
        args, _ = parser.parse_known_args()
        cls.__management_command = args.command
