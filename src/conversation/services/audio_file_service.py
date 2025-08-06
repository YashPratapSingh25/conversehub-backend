from pathlib import Path
import aiofiles
from fastapi import UploadFile
import tempfile

tmp_audio_directory = tempfile.gettempdir()

async def create_audio_file(file : UploadFile):
    suffix = Path(file.filename).suffix
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tmp_audio_directory)
    temp_path = temp_file.name
    temp_file.close()

    async with aiofiles.open(temp_path, "wb") as new_audio_file:
        content = await file.read()
        await new_audio_file.write(content)

    return temp_path