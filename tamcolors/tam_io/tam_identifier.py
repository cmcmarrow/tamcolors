import platform
import subprocess
from tamcolors.tam_io import win_drivers
from tamcolors.tam_io import any_drivers


class TAMIdentifier:
    def __init__(self,
                 name=None,
                 color_driver=None,
                 color_change_driver=None,
                 key_driver=None,
                 utilities_driver=None):

        if name is None:
            name = "UNKNOW"

        if color_driver is None:
            color_driver = any_drivers.ANYColorDriver

        if color_change_driver is None:
            color_change_driver = any_drivers.ANYColorChangerDriver

        if key_driver is None:
            key_driver = any_drivers.ANYKeyDriver

        if utilities_driver is None:
            utilities_driver = any_drivers.ANYUtilitiesDriver

        self._name = name
        self._color_driver = color_driver
        self._color_change_driver = color_change_driver
        self._key_driver = key_driver
        self._utilities_driver = utilities_driver
        self._system = platform.system()

    def __str__(self):
        output = ""
        info = self.get_info_dict()
        for key in info:
            output += "{}:\t\t\t{}\n".format(key, info[key])
        return output

    def get_name(self):
        return self._name

    def get_color_driver(self):
        return self._color_driver

    def get_color_change_driver(self):
        return self._color_change_driver

    def get_key_driver(self):
        return self._key_driver

    def get_utilities_driver(self):
        return self._utilities_driver

    def get_all_drivers(self):
        return (self.get_color_driver(),
                self.get_color_change_driver(),
                self.get_key_driver(),
                self.get_utilities_driver())

    def get_system(self):
        return self._system

    def get_info_dict(self):
        return {"name": self.get_name(),
                "color_driver": self.get_color_driver().__name__,
                "color_change_driver": self.get_color_change_driver().__name__,
                "key_driver": self.get_key_driver().__name__,
                "utilities_driver": self.get_utilities_driver().__name__,
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

        if EnvironmentIO.able_to_execute():
            return EnvironmentIO(identifier=self)


ANY_IO = TAMIdentifier().build_io()
IO = TAMIdentifier.identify().build_io()
