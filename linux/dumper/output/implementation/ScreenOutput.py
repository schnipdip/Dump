from linux.dumper.output.Output import Output


class ScreenOutput(Output):
    def print(self, message, timeout: float = .5):
        # ScreenOutput ignores timeout
        print(message)
