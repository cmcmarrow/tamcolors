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
            # out of free ids
            if not self._free_ids:
                # make new id
                active_id = len(self._used_ids)
                self._used_ids.add(active_id)
            else:
                # reuse free id
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
            # id is not being used
            if active_id not in self._used_ids:
                return False

            # free id
            self._used_ids.remove(active_id)
            self._free_ids.add(active_id)

            # clear all ids
            if not self._used_ids:
                self._free_ids.clear()
        finally:
            self._lock.release()
        return True
