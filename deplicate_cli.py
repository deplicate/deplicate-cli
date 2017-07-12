# -*- coding: utf-8 -*-
#
#          _/                   _/ _/                     _/
#     _/_/_/   _/_/   _/_/_/   _/     _/_/_/    _/_/_/ _/_/_/_/   _/_/
#  _/    _/ _/_/_/_/ _/    _/ _/ _/ _/       _/    _/   _/     _/_/_/_/
# _/    _/ _/       _/    _/ _/ _/ _/       _/    _/   _/     _/
#  _/_/_/   _/_/_/ _/_/_/   _/ _/   _/_/_/   _/_/_/     _/_/   _/_/_/
#                 _/
#                _/

from __future__ import absolute_import

import pkg_resources
import time

import click
import duplicate

from contextlib import closing
from multiprocessing.pool import ThreadPool


def _get_separator():
    return '{{0:-^{0}}}'.format(click.get_terminal_size()[0])


def _echo_results(results, verbose, showerr):
    dups, errors, scanerrors = results

    sep = _get_separator()

    if verbose:
        click.secho(sep.format('  DUPLICATES  '), bold=True)
        click.echo()

    with closing(ThreadPool()) as pool:
        for files in dups:
            pool.map(click.echo, files)
            click.echo()

        if not showerr:
            return

        click.echo()
        if verbose:
            click.secho(sep.format('  PROCESS ERRORED  '), bold=True)
            click.echo()

        for files in errors:
            map(click.echo, files)

        click.echo()
        if verbose:
            click.secho(sep.format('  SCAN ERRORED  '), bold=True)
            click.echo()

        map(click.echo, scanerrors)


def _notifier(message):
    click.secho('  Done.', fg='green')
    text = '> {0}...'.format(message.capitalize())
    click.echo(text, nl=False)


def _get_deplicate_version():
    return pkg_resources.get_distribution('deplicate').version
    
    
def _find_results(verbose, kwgs):
    core = duplicate.core
    paths = kwgs.pop('paths')

    if verbose > 2:
        text = '> Starting deplicate (v{0})...'
        click.echo(text.format(_get_deplicate_version()), nl=False)
        kwgs['notify'] = _notifier

    start_time = time.time()

    filedups, scanerrors = core._find(paths, **kwgs)

    dups = core._listdups(filedups)
    errors = core._listerrors(filedups)

    elapsed_seconds = time.time() - start_time
    formatted_seconds = _format_seconds(elapsed_seconds)

    if verbose > 2:
        click.secho('  Done.', fg='green')
        click.echo()

        if verbose > 3:
            sep = _get_separator()
            click.secho(sep.format('  STATISTICS  '), bold=True)
            click.echo()

            text = 'Completed in {0:f} seconds ({1}).'
            click.echo(text.format(elapsed_seconds, formatted_seconds))
            click.echo()

    return dups, errors, scanerrors


def _format_seconds(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    text = '{0} days, {1} hours, {2} minutes, {3} seconds'
    return text.format(d, h, m, s)


def _cli(verbose, showerr, kwgs):
    if verbose:
        click.echo()

    dups, errors, scanerrors = results = _find_results(verbose, kwgs)

    if verbose:
        with closing(ThreadPool()) as pool:
            duplen = sum(pool.imap(len, dups))
            errlen = sum(pool.imap(len, errors))
        scnerrlen = len(scanerrors)

        if not showerr and (errlen or scnerrlen):
            text = '>> Errors detected during processing! ' \
                   '(use option `--show-errors` to report errors)'
            click.secho(text, fg='red')
            click.echo()

        if verbose > 1:
            if verbose > 2:
                sep = _get_separator()
                click.secho(sep.format('  RESULT  '), bold=True)
                click.echo()

            if errlen or scnerrlen:
                color = 'yellow'
            elif duplen:
                color = 'reset'
            else:
                color = 'green'

            click.secho('Found {0} duplicate files.'.format(duplen), fg=color)
            click.echo()

            if showerr:
                color = 'red' if errlen else 'green'
                click.secho('Failed to process {0} files.'.format(errlen),
                            fg=color)

                color = 'red' if scnerrlen else 'green'
                click.secho('Failed to scan {0} files.'.format(scnerrlen),
                            fg=color)
                click.echo()

    _echo_results(results, verbose, showerr)


@click.command()
@click.argument('paths',
                type=click.Path(exists=True),
                nargs=-1)
@click.option('--verbose', '-v',
              count=True,
              help='Verbose mode (repeat to increase verbosity).')
@click.option('--show-errors', '-a',
              is_flag=True,
              help='Show ignored files due errors.')
@click.option('--minsize', '-s',
              type=click.IntRange(min=0, clamp=True),
              default=None,
              help='Minimum size of files to include in scanning.')
@click.option('--include', '-i',
              help='Wildcard pattern of files to include in scanning.')
@click.option('--exclude', '-e',
              help='Wildcard pattern of files to exclude from scanning.')
@click.option('--comparename', '-n',
              is_flag=True,
              help='Check file name.')
@click.option('--comparemtime', '-m',
              is_flag=True,
              help='Check file modification time.')
@click.option('--compareperms', '-p',
              is_flag=True,
              help='Check file mode (permissions).')
@click.option('--recursive/--no-recursive',
              default=True,
              help='Scan directory recursively.')
@click.option('--followlinks',
              is_flag=True,
              help='Follow symbolic links pointing to directory.')
@click.option('--scanlinks',
              is_flag=True,
              help='Scan symbolic links pointing to file.')
@click.option('--scanempties',
              is_flag=True,
              help='Scan empty files.')
@click.option('--scansystems/--ignoresystems',
              default=True,
              help='Scan OS files.')
@click.option('--scanarchived/--ignorearchived',
              default=True,
              help='Scan archived files.')
@click.option('--scanhidden/--ignorehidden',
              default=True,
              help='Scan hidden files.')
@click.option('--signsize',
              type=click.IntRange(min=0, clamp=True),
              default=None,
              help='Size of Bytes to read from file as signature.')
@click.version_option()
def cli(**kwgs):
    """
    Advanced Duplicate File Finder for Python. Nothing is impossible to solve.

    Copyright 2017 Walter Purcaro <vuolter@gmail.com>
    """
    verbose = kwgs.pop('verbose')
    showerr = kwgs.pop('show_errors')
    _cli(verbose, showerr, kwgs)
