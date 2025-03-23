import click

class DefaultRunGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        cmd = super().get_command(ctx, cmd_name)
        if cmd:
            return cmd
        return self.get_default_command(ctx, cmd_name)

    def get_default_command(self, ctx, cmd_name):
        def fallback_cmd(**kwargs):
            from techies.cli.utils.dispatch import kickoff_default_crew
            kickoff_default_crew(cmd_name)
        return click.Command(cmd_name, callback=fallback_cmd, help="Run a default crew.")
