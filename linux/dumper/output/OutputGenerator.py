from linux.dumper.output.Output import Output
from linux.dumper.output.exception.OutputException import OutputException
from linux.dumper.output.implementation.LcdOutput import LcdOutput
from linux.dumper.output.implementation.ScreenOutput import ScreenOutput

MONITOR = "monitor"
LCD = "lcd"
DISPLAY_TYPES = [MONITOR, LCD]


def get(display: str) -> Output:
    if display not in DISPLAY_TYPES: raise OutputException("Undefined output type")
    if display == MONITOR: return ScreenOutput()
    if display == LCD: return LcdOutput()
