import yaml
import json
import pkgutil
import jsonschema
import jsonschema.exceptions


from airbyte_cdk.sources.declarative.parsers.manifest_reference_resolver import (
    ManifestReferenceResolver,
)
from airbyte_cdk.sources.declarative.parsers.manifest_component_transformer import (
    ManifestComponentTransformer,
)


with open(
    "/Users/morgan.kerle/data/data-platforms/airbyte-connectors/async-api-connector/schemas/declarative_component_schema.yaml",
    "r",
) as f:
    declarative_component_schema = yaml.load(f, Loader=yaml.SafeLoader)

with open(
    "/Users/morgan.kerle/data/data-platforms/airbyte-connectors/async-api-connector/async_api_connector/manifest.yaml"
) as file:
    manifest = yaml.safe_load(file)

resolved_source_config = ManifestReferenceResolver().preprocess_manifest(manifest)
propagated_source_config = (
    ManifestComponentTransformer().propagate_types_and_parameters(
        "", resolved_source_config, {}
    )
)

validator = jsonschema.Draft7Validator(declarative_component_schema)

errors = validator.iter_errors(propagated_source_config)


# for error in sorted(errors, key=lambda e: e.path):
#     for suberror in sorted(error.context, key=jsonschema.exceptions.relevance):
#         print(suberror)

# error_tree = jsonschema.ErrorTree(validator.iter_errors(propagated_source_config))

for error in sorted(errors, key=lambda e: e.path):
    print(f"Error in {list(error.path)}: {error.message}")
    print(f"  Schema path: {list(error.schema_path)}")
    print(f"  Instance: {error.instance}")
    for suberror in sorted(error.context, key=jsonschema.exceptions.relevance):
        print(f"  Suberror in {list(suberror.path)}: {suberror.message}")
        print(f"    Schema path: {list(suberror.schema_path)}")
        print(f"    Instance: {suberror.instance}")

error_tree = jsonschema.ErrorTree(validator.iter_errors(propagated_source_config))

if "streams" in error_tree:
    print("Errors in 'streams':")
    for path, error in error_tree["streams"].errors.items():
        print(f"  {path}: {error.message}")
        print(f"    Schema path: {list(error.schema_path)}")
        print(f"    Instance: {error.instance}")

with open("resolved_manifest.json", "w") as file:
    json.dump(resolved_source_config, file, indent=2)

with open("propagated_manifest.json", "w") as file:
    json.dump(propagated_source_config, file, indent=2)
