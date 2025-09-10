"""DynamicsBusinessCentral Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


class DynamicsBusinessCentralAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for DynamicsBusinessCentral."""

    @property
    def oauth_request_body(self) -> dict:
        return {
            "scope": self.config["oauth_scopes"],
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "grant_type": "client_credentials",
        }

    @classmethod
    def create_for_stream(cls, stream) -> DynamicsBusinessCentralAuthenticator:  # noqa: ANN001
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            stream=stream,
            auth_endpoint=stream.config["auth_url"],
            oauth_scopes=stream.config["oauth_scopes"],
        )
