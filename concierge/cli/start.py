from concierge import app
from concierge.cli import CommandFactory


class StartCommand(CommandFactory):
    def __init__(self, parser, *args, **kwargs):
        self.parser = parser.add_parser(*args, **kwargs)
        self.parser.set_defaults(action=self.run)

        self.components = [
            "bot",
            "server"
        ]

        # Components
        self.parser.add_argument(
            "--component",
            required=True,
            choices=self.components,
            help="Specify the type of component to start."
        )

        # Set Logging Levels
        self.choices = [
            "spam",
            "debug",
            "verbose",
            "info",
            "notice",
            "warning",
            "success",
            "error",
            "critical",
        ]
        self.parser.add_argument(
            "--log", choices=self.choices, type=str.lower, help="amount of info to log"
        )

    def run(self, *sys_args):
        passed_args = {"component": None, "log_level": None}
        if len(sys_args) > 0:
            if sys_args[0].log:
                passed_args["log_level"] = sys_args[0].log

            if sys_args[0].component:
                passed_args["component"] = sys_args[0].component
                if passed_args["component"] == "server":
                    app.start_server(**passed_args)
                elif passed_args["component"] == "bot":
                    app.start_bot(**passed_args)
