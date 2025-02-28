from google.cloud import secretmanager
from .common import logger

def get_secret_value(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Retrieve the actual value of a secret from Google Cloud Secret Manager.
    
    Args:
        project_id: The GCP project ID containing the secret
        secret_id: The ID of the secret to retrieve
        version_id: The version of the secret to retrieve (defaults to "latest")
    
    Returns:
        The secret value as a string
    
    Raises:
        Exception: If there's an error accessing the secret
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
        
    except Exception as e:
        raise logger.error(f"Failed to retrieve secret {secret_id}: {str(e)}")