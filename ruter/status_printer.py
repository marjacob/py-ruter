# -*- coding: utf-8 -*-


import click


class StatusPrinter(object):
    def action(self, message):
        prefix = click.style("[ .. ]", bold=True, fg="blue")
        click.echo("\r{0} {1}...".format(prefix, message))
    
    def error(self, message):
        prefix = "{left_bracket} {stars} {right_bracket}".format(
            left_bracket=click.style("[", bold=True, fg="blue"),
            stars=click.style("**", bold=False, fg="red"),
            right_bracket=click.style("]", bold=True, fg="blue"))
        click.echo("\r{prefix} {message}".format(prefix=prefix, message=message))
    
    def message(self, message, bold=False):
        prefix = "{left_bracket} {stars} {right_bracket}".format(
            left_bracket=click.style("[", bold=True, fg="blue"),
            stars=click.style("**", bold=False, fg="yellow"),
            right_bracket=click.style("]", bold=True, fg="blue"))
        if bold:
            message = click.style(message, bold=True)
        click.echo("\r{prefix} {message}".format(prefix=prefix, message=message))
    
    def status(self, success, message=None):
        prefix = None
        if success:
            if not message:
                message = "OK"
            else:
                message = "OK [{0}]".format(message)
            prefix = "{left_bracket} {angles} {right_bracket}".format(
                left_bracket=click.style("[", bold=True, fg="blue"),
                angles=click.style(">>", bold=False, fg="green"),
                right_bracket=click.style("]", bold=True, fg="blue"))
        else:
            prefix = "{left_bracket} {angles} {right_bracket}".format(
                left_bracket=click.style("[", bold=True, fg="blue"),
                angles=click.style("!!", bold=True, fg="red"),
                right_bracket=click.style("]", bold=True, fg="blue"))
            message = message if message else "Failed"
            message = click.style(message, bold=True, fg="red")
        click.echo("\r{prefix} {message}".format(prefix=prefix, message=message))



