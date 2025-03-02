import os, sys, io
import logging


class MyLogger:
    def __init__(self, log_path="./log.txt"):
        """
        only allows 3 levels
        - info
        - warning (by default)
        - error
        """

        # create folder and file
        if log_path:
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            with open(log_path, "w") as _:
                pass

        # use root logger
        self.logger = logging.getLogger()

        # remove existing handlers
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        # print to stdout
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        # stdout_handler.flush = True
        stdout_handler.setLevel(logging.INFO)
        self.logger.addHandler(stdout_handler)

        # print to file
        if log_path:
            file_handler = logging.FileHandler(filename=log_path, encoding="utf-8", delay=False)
            # file_handler.flush = True
            file_handler.setFormatter(logging.Formatter("# %(asctime)s - %(levelname)s\n%(message)s"))
            file_handler.setLevel(logging.INFO)
            self.logger.addHandler(file_handler)

    def pseudo_print(self, *args, **kwargs):
        for print_kwarg in ("file", "flush"):
            if print_kwarg in kwargs:
                kwargs.pop(print_kwarg, None)
        for print_kwarg, default_value in (("end", ""),):
            if not print_kwarg in kwargs:
                kwargs[print_kwarg] = default_value
        pseudo_file = io.StringIO()
        print(*args, **kwargs, file=pseudo_file, flush=False)
        return pseudo_file.getvalue()

    def info(self, *args, **kwargs):
        message = self.pseudo_print(*args, **kwargs)
        self.logger.info(message)

    def warning(self, *args, **kwargs):
        message = self.pseudo_print(*args, **kwargs)
        self.logger.warning(message)

    def __call__(self, *args, **kwargs):
        self.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        message = self.pseudo_print(*args, **kwargs)
        self.logger.error(message)


if __name__ == "__main__":
    logger = MyLogger(log_path=None)
    logger("as if this is a print function", {"amy": 0, "bob": 1, "cas": 2}, sep="\n")
