import sys

from airbyte_cdk.entrypoint import launch

from .source import AsyncApiSource


def run():
    source = AsyncApiSource()
    launch(source, sys.argv[1:])
