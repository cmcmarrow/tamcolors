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

    def __str__(self):
        output = ""
        info = self.get_info_dict()
        for key in info:
            output += "{}:\t\t\t{}\n".format(key, info[key])
        return output

    def get_name(self):
        return self._name

    def get_all_drivers(self):
        return self._drivers.copy()

    def get_system(self):
        return self._system

    def get_info_dict(self):
        # TODO fix drivers
        return {"name": self.get_name(),
                "drivers": self.get_all_drivers(),
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
                               win_drivers.WINColorDriver,
                               win_drivers.WINColorChangerDriver,
                               win_drivers.WINKeyDriver,
                               win_drivers.WINUtilitiesDriver)
            except FileNotFoundError:
                pass

        if guess:
            guess_identifier = cls._guess()
            if guess_identifier is not None:
                return guess_identifier

        return ANY_IO

    @classmethod
    def _guess(cls):
        pass

    def build_io(self):
        class EnvironmentIO(*self.get_all_drivers()):
            pass

        return EnvironmentIO(identifier=self)


#ANY_IO = TAMIdentifier("UNKNOW").build_io()
IO = TAMIdentifier.identify().build_io()
