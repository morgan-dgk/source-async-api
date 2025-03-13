from typing import Literal, Optional, Union

from airbyte_cdk.utils.oneof_option_config import OneOfOptionConfig
from airbyte_cdk.sources.config import BaseConfig
from pydantic.v1 import BaseModel, Field


class SessionTokenCredentials(BaseModel):
    class Config(OneOfOptionConfig):
        title = "Session Token"
        discriminator = "auth_type"

    auth_type: Literal["Session Token"] = Field("Session Token", const=True)

    username: str = Field(
        ..., title="Username", description="The username to use to authenticate."
    )
    password: str = Field(
        ..., title="Password", description="The password to use to authenticate."
    )
    session_token_login_path: str = Field(
        ...,
        title="Session Token Login Path",
        description="The path to use to login and get a session token.",
    )
    session_token_path: str = Field(
        ...,
        title="Session Token Path",
        description="Path in login response which contains session token.",
    )


class BasicAuthCredentials(BaseModel):
    class Config(OneOfOptionConfig):
        title = "Basic Auth"
        discriminator = "auth_type"

    auth_type: Literal["HTTP Basic"] = Field("HTTP Basic", const=True)
    username: str = Field(
        ..., title="Username", description="The username to use to authenticate."
    )
    password: str = Field(
        ...,
        title="Password",
        description="The password to use to authenticate.",
        airbyte_secret=True,
    )


class SourceAsyncApiSpec(BaseConfig):
    class Config:
        title = "Async Api Source Spec"
        use_enum_values = True

    credentials: Union[SessionTokenCredentials, BasicAuthCredentials] = Field(
        title="Authentication",
        description="Credentials to use when authenticate with API.",
        discriminator="auth_type",
        type="object",
        order=0,
    )

    create_request_path: str = Field(
        ...,
        title="Create Request Path",
        description="API path to send create request.",
        order=1,
    )

    polling_request_path: str = Field(
        ...,
        title="Polling Request Path",
        description="API path to poll for job status.",
        order=2,
    )

    url_extractor_path: str = Field(
        ...,
        title="URL Extractor Path",
        description="Path in completed response with download URL / fragment.",
        order=3,
    )

    download_request_path: str = Field(
        ...,
        title="Download Request Path",
        description="Path to download API response.",
        order=4,
    )

    status_path: str = Field(
        ...,
        title="Status Path",
        description="Path to API status in JSON response from polling request.",
        order=5,
    )

    create_request_body_json: Optional[str] = Field(
        ...,
        description="JSON payload to send to the API when submitting a create request.",
        title="JSON Payload for Create Request",
        airbyte_secret=False,
        order=6,
    )
