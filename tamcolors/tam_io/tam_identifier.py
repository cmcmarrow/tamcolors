import platform
import subprocess
from tamcolors.tam_io import win_drivers
from tamcolors.tam_io import any_drivers
from tamcolors.tam_io import tam_drivers


class TAMIdentifier:
    def __init__(self,
                 name,
                 *drivers):

        self._name = name
        self._drivers = list(drivers)
        self._system = platform.system()
        self._environment_io = None

    def __str__(self):
        output = ""
        info = self.get_info_dict()
        for key in info:
            data = info[key]
            if isinstance(data, (list, tuple)):
                data = "\n\t".join(data)
            output += "{}:\n\t{}\n".format(key, data)

        if len(output) != 0:
            output = output[:-1]
        return output

    def get_name(self):
        return self._name

    def get_all_drivers(self):
        return self._drivers.copy()

    def get_system(self):
        return self._system

    def get_info_dict(self):
        return {"name": self.get_name(),
                "drivers": [driver.__name__ for driver in self.get_all_drivers()],
                "system": self.get_system()}

    @classmethod
    def identify(cls, guess=True):
        if platform.system().lower() == "windows":
            try:
                name = str(subprocess.run("(dir 2>&1 *`|echo cmd);&<# rem #>echo PowerShell",
                                          shell=True,
                                          capture_output=True).stdout, encoding="utf-8").strip("\n").strip("\r")
                if name in ("cmd", "PowerShell"):
                    return cls(name,
                               win_drivers.WINFullColorDriver,
                               win_drivers.WINKeyDriver,
                               win_drivers.WINUtilitiesDriver)
            except FileNotFoundError:
                pass

        if guess:
            guess_identifier = cls._guess()
            if guess_identifier is not None:
                return guess_identifier

        return ANY_IO_IDENTIFIER

    @classmethod
    def _guess(cls):
        name = "GUESS"
        if platform.system().lower() == "windows":
            if win_drivers.WinSharedData.able_to_execute():
                return cls(name,
                           win_drivers.WINFullColorDriver,
                           win_drivers.WINKeyDriver,
                           win_drivers.WINUtilitiesDriver)

    def build_io(self):
        if self._environment_io is None:
            class EnvironmentIO(*self.get_all_drivers()):
                pass
            self._environment_io = EnvironmentIO(identifier=self)
        return self._environment_io


ANY_IO_IDENTIFIER = TAMIdentifier("UNKNOW",
                                  any_drivers.ANYKeyDriver,
                                  any_drivers.ANYColorDriver,
                                  any_drivers.ANYColorChangerDriver,
                                  any_drivers.ANYUtilitiesDriver)

ANY_IO = ANY_IO_IDENTIFIER.build_io()
IO = TAMIdentifier.identify().build_io()
