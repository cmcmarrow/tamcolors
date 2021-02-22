from threading import Lock


class IDManager:
    def __init__(self):
        self._used_ids = set()
        self._free_ids = set()
        self._lock = Lock()

    def get_id(self):
        """
        info: will get id
        :return: int
        """
        try:
            self._lock.acquire()
            if not self._free_ids:
                active_id = len(self._used_ids)
                self._used_ids.add(active_id)
            else:
                active_id = self._free_ids.pop()
                self._used_ids.add(active_id)
        finally:
            self._lock.release()
        return active_id

    def free_id(self, active_id):
        """
        info: will free an id
        :return: bool
        """
        try:
            self._lock.acquire()
            if active_id not in self._used_ids:
                return False
            self._used_ids.add(active_id)
            self._free_ids.add(active_id)
        finally:
            self._lock.release()
        return True
