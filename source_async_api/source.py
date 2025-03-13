import logging

from airbyte_cdk.models import ConnectorSpecification
from airbyte_cdk.sources.declarative.yaml_declarative_source import (
    YamlDeclarativeSource,
)

from .spec import SourceAsyncApiSpec


class AsyncApiSource(YamlDeclarativeSource):
    def __init__(self):
        super().__init__(**{"path_to_yaml": "manifest.yaml"})

    def spec(self, logger: logging.Logger) -> ConnectorSpecification:
        return ConnectorSpecification(
            documentationUrl="https://docs.airbyte.io/integrations/sources/async-api",
            connectionSpecification=SourceAsyncApiSpec.schema(),
        )
