from google.cloud import secretmanager


class GcpSecretManager:
    _gcp_project_id = "whatever-your-project-is"
    _client = None

    def __init__(self):
        self._client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str):
        name = f"projects/{self._gcp_project_id}/secrets/{secret_id}/versions/latest"
        response = self._client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
