# built in libraries
import threading
import multiprocessing
import collections


def process_runner(error_ret, func, *args, **kwargs):
    """
    info: will run the task
    :param error_ret: list: away to return an error
    :param func: function
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    try:
        func(*args, **kwargs)
    except Exception as e:
        error_ret.put(e)


class MultiTaskHelper:
    _Task = collections.namedtuple("Task", ("func", "args", "kwargs"))

    def multiple_threads_helper(self, tasks, timeout=120):
        """
        info: will run tasks in a thread
        :param tasks: list or tuple: [(func, tuple, dict), ...]
        :param timeout: int
        :return:
        """
        def _not_main_task(task, time):
            """
            info: will run task in a thread and return an error
            :param task: tuple or list: (func, tuple, dict)
            :param time:
            :return: Exception or None
            """
            error = []

            def thread_runner(error_ret, func, *args, **kwargs):
                """
                info: will run the task
                :param error_ret: list: away to return an error
                :param func: function
                :param args: tuple
                :param kwargs: dict
                :return:
                """
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    error_ret.append(e)

            try:
                thread = threading.Thread(target=thread_runner,
                                          args=(error, task.func,) + task.args,
                                          kwargs=task.kwargs,
                                          daemon=True)
                thread.start()
                thread.join(timeout=time)

                # return error
                if error:
                    return error[0]
            except Exception as e:
                return e

        self._multiple_helper(tasks, _not_main_task, timeout)

    def multiple_processes_helper(self, tasks, timeout=120):
        """
        info: will run tasks in a thread
        :param tasks: list or tuple: [(func, tuple, dict), ...]
        :param timeout: int
        :return:
        """
        def _not_main_task(task, time):
            """
            info: will run task in a thread and return an error
            :param task: tuple or list: (func, *args, **kwargs)
            :param time:
            :return: Exception or None
            """
            error = multiprocessing.Queue()

            process = multiprocessing.Process(target=process_runner,
                                              args=(error, task.func,) + task.args,
                                              kwargs=task.kwargs,
                                              daemon=True)
            try:
                process.start()
                process.join(timeout=time)

                # return error
                if not error.empty():
                    return error.get()
            except Exception as e:
                return e

        self._multiple_helper(tasks, _not_main_task, timeout)

    @staticmethod
    def _multiple_helper(tasks, not_main_task, timeout):
        def runner(this_task, error_list):
            """
            info: will run a task
            :param this_task: Task
            :param error_list: list
            :return: Thread
            """
            def runner_thread():
                """
                info: runner thread
                :return:
                """
                try:
                    task_error = not_main_task(this_task, timeout)
                    if task_error is not None:
                        error_list.append(task_error)
                except Exception as e:
                    error_list.append(e)

            thread = threading.Thread(target=runner_thread, daemon=True)
            thread.start()
            return thread

        # run every task as the main task
        for main_spot, main_task in enumerate(tasks):
            errors = []
            threads = []
            # run every other task as not the main task
            for spot, task in enumerate(tasks):
                if main_spot != spot:
                    threads.append(runner(task, errors))

            main_task.func(*main_task.args, **main_task.kwargs)
            # wait for all threads to return
            for done_thread in threads:
                done_thread.join(timeout)

            # check if any errors where raised
            if errors:
                raise errors[0]

    @classmethod
    def task(cls, func, *args, **kwargs):
        """
        info: will make a Task
        :param func: Function
        :param args: tuple
        :param kwargs: dict
        :return: Task
        """
        return cls._Task(func, args, kwargs)
