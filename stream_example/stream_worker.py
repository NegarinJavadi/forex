import os
main_dir = os.path.join(os.path.dirname(__file__), '..')
import sys
sys.path.insert(0,main_dir)

from collections.abc import Callable, Iterable, Mapping
from queue import Queue
import threading
import time
from typing import Any
from infrastructure.log_wrapper import LogWrapper
from models.live_api_price import LiveApiPrice


class WorkProcessor(threading.Thread):

    def __init__(self, work_queue:Queue):
        super().__init__()
        self.work_queue = work_queue
        self.log = LogWrapper("WorkProcessor")

    def run(self):
        while True:
            work: LiveApiPrice = self.work_queue.get()
            self.log.logger.debug(f"New Work: {work}")
            time.sleep(7)