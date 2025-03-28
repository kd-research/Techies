import click

class DefaultRunGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        cmd = super().get_command(ctx, cmd_name)
        if cmd:
            return cmd
        return self.get_default_command(ctx, cmd_name)

    def get_default_command(self, ctx, cmd_name):
        @click.command(cmd_name)
        @click.argument('args', nargs=-1, required=False)
        def fallback_cmd(*_, **kwargs):
            from techies.cli.utils.dispatch import kickoff_default_crew
            
            # Get extra arguments from context
            extra_args = kwargs.get('args', [])
            
            click.echo(f"Running default crew for {cmd_name} with args: {extra_args}")
            kickoff_default_crew(cmd_name, extra_args=extra_args)
            
        #return click.Command(cmd_name, callback=fallback_cmd, help="Run a default crew.")
        return fallback_cmd