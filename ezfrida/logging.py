#!/usr/bin/python3

import logging
import os
import time

from colorama import Fore, Style
from datetime import datetime
from pathlib import Path


class ConsoleFormatter(logging.Formatter):

    FORMATS = {
        logging.DEBUG: Fore.CYAN  + " [~] (%(asctime)s) %(message)s" + Style.RESET_ALL,
        logging.INFO: Fore.GREEN  + " [-] (%(asctime)s) %(message)s" + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW  + " [+] (%(asctime)s) %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + " [!] (%(asctime)s) %(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + " [!] (%(asctime)s) %(message)s" + Style.RESET_ALL,
        "DEFAULT": " [ ] (%(asctime)s) %(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)


class FileFormatter(logging.Formatter):

    FORMATS = {
        logging.WARNING: "[WARN]\t(%(asctime)s) %(message)s",
        logging.CRITICAL: "[CRIT]\t(%(asctime)s) %(message)s",
        "DEFAULT": "[%(levelname)s]\t(%(asctime)s) %(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


def setup_logging(log_to_file=False, debug=False):
    """
    Set up logging.
    """
    logger = logging.getLogger()
    if debug:
        logger.setLevel('DEBUG')
    else:
        logger.setLevel('INFO')
    logger_ch = logging.StreamHandler()
    logger_ch.setFormatter(ConsoleFormatter())
    logger.addHandler(logger_ch)
    if log_to_file:
        logfile = (os.path.join(os.getcwd(), 'ezfrida-' + str(int(time.time())) + '.log'))
        logger_fh = logging.FileHandler(logfile, mode='w')
        logger_fh.setFormatter(FileFormatter())
        logger.addHandler(logger_fh)
    logger.info('Logging set up successfully')
    return logger