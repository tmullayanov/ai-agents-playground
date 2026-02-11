from pathlib import Path
from urllib.parse import ParseResult, urlparse
import mimetypes
from loguru import logger

import requests

session = requests.Session()
session.verify = False


def load_file(source: str, timeout: float = 30.0) -> tuple[str, bytes, str]:
    """
    Load file either from URL or local path
    """

    logger.info("Starting file load")
    logger.debug(f"Source: {source}")

    parsed = urlparse(source)

    if parsed.scheme in ("http", "https"):
        logger.info("Loading file from URL")
        return load_file_from_url(source, timeout, parsed)
    else:
        logger.info("Loading file from local path")
        return load_file_from_path(source)
    
def load_file_from_url(source: str, timeout: float, parsed: ParseResult) -> tuple[str, bytes, str]:
    try:
        response = session.get(source, timeout=timeout)
        logger.debug(
            "HTTP Response received",
            status_code=response.status_code,
            headers=response.headers
        )
        response.raise_for_status()

        content = response.content
        filename = Path(parsed.path).name if parsed.path else "downloaded_file"
        logger.debug(f"Resolved filename: {filename}")

        mime_type = response.headers.get("Content-Type")
        if mime_type:
            mime_type = mime_type.split(";")[0]
            logger.debug(f"MIME type from headers: {mime_type}")
        else:
            mime_type = _guess_mime(filename)
            logger.warning(
                "MIME type missing in headers, guessed instead",
                guessed_mime=mime_type
            )

        logger.info("Remote file loaded successfully")
        return filename, content, mime_type
    except Exception as e:
        logger.error(f"Error loading file from URL: {e}")
        raise

def load_file_from_path(source: str) -> tuple[str, bytes, str]:
    try:
        path = Path(source).expanduser().resolve()
        logger.debug(f"Resolved path: {path}")

        if not path.exists():
            logger.error("File does not exist", path=str(path))
            raise FileNotFoundError(f"File not found: {path}")
        
        if not path.is_file():
            logger.error("Path is not a file", path=str(path))
            raise IsADirectoryError(f"Not a file: {path}")
        
        content = path.read_bytes()
        logger.debug(f"Read {len(content)} bytes")

        filename = path.name
        mime_type = _guess_mime(filename)

        logger.info("Local file loaded successfully")
        return filename, content, mime_type
    except Exception as e:
        logger.error(f"Error loading file from path: {e}")
        raise


def _guess_mime(filename: str) -> str:

    mime_type, _ = mimetypes.guess_type(filename)
    mime_type = mime_type or "application/octet-stream"

    #if mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
    #    return "SPREADSHEET"
    
    return mime_type