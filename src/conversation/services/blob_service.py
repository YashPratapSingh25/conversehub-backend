import asyncio
from datetime import datetime, timedelta, timezone
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions, ContentSettings
import aiofiles
from src.core.config import settings

async def generate_sas_token(user_id, session_id, turn_id, user : bool):
    blob_base_url = f"user_{user_id}/session_{session_id}/"
    blob_name = f"{blob_base_url}user_{turn_id}.wav" if user else f"{blob_base_url}ai_{turn_id}.wav"

    sas_token = await asyncio.to_thread(
        generate_blob_sas,
        account_name=settings.AZURE_STORAGE_ACCOUNT_NAME,
        container_name="audiofiles",
        blob_name=blob_name,
        account_key=settings.AZURE_STORAGE_ACCOUNT_KEY,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(timezone.utc) + timedelta(hours=1)
    )

    sas_url = f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/audiofiles/{blob_name}?{sas_token}"
    return sas_url


async def upload_file_and_get_sas(user_id, session_id, turn_id, file_path, user : bool):

    blob_service = BlobServiceClient.from_connection_string(settings.AZURE_BLOB_CONN_STRING)

    blob_base_url = f"user_{user_id}/session_{session_id}/"

    blob_client = blob_service.get_blob_client(
        container="audiofiles", 
        blob=f"{blob_base_url}user_{turn_id}.wav" if user else f"{blob_base_url}ai_{turn_id}.wav"
    )
    
    async with aiofiles.open(file_path, "rb") as new_file:
        file_data = await new_file.read()

        content_settings = ContentSettings(
            content_type = 'audio/wav',
            content_disposition = 'inline',
        )

        await asyncio.to_thread(blob_client.upload_blob, file_data, content_settings=content_settings, overwrite=True)

    sas_url = await generate_sas_token(user_id, session_id, turn_id, user)

    return sas_url