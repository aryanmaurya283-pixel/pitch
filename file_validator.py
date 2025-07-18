import os
import re
from typing import Tuple, Optional

# Try to import magic, fallback if not available
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

from config import config

def validate_file_size(file_size: int) -> Tuple[bool, Optional[str]]:
    """Validate file size is within acceptable limits."""
    if file_size < config.file.MIN_FILE_SIZE:
        return False, f"File too small. Minimum size is {config.file.MIN_FILE_SIZE} bytes."
    
    if file_size > config.file.MAX_FILE_SIZE:
        return False, f"File too large. Maximum size is {config.file.MAX_FILE_SIZE // (1024*1024)}MB."
    
    return True, None

def validate_file_extension(filename: str) -> Tuple[bool, Optional[str]]:
    """Validate file has an allowed extension."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in config.file.ALLOWED_MIME_TYPES:
        return False, f"File type '{ext}' not allowed. Supported types: {', '.join(config.file.ALLOWED_MIME_TYPES.keys())}"
    
    return True, None

def validate_filename(filename: str) -> Tuple[bool, Optional[str]]:
    """Validate filename doesn't contain malicious patterns."""
    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False, "Invalid filename. Path traversal detected."
    
    # Check for suspicious characters
    if re.search(r'[<>:"|?*]', filename):
        return False, "Invalid filename. Contains forbidden characters."
    
    # Check filename length
    if len(filename) > 255:
        return False, "Filename too long. Maximum 255 characters."
    
    return True, None

def validate_mime_type(file_path: str, expected_extension: str) -> Tuple[bool, Optional[str]]:
    """Validate file MIME type matches extension."""
    if not MAGIC_AVAILABLE:
        return True, "Warning: MIME type validation skipped (python-magic not available)"
    
    try:
        # Get MIME type using python-magic
        mime_type = magic.from_file(file_path, mime=True)
        
        allowed_mimes = config.file.ALLOWED_MIME_TYPES.get(expected_extension, [])
        
        if mime_type not in allowed_mimes:
            return False, f"File content doesn't match extension. Expected: {allowed_mimes}, Got: {mime_type}"
        
        return True, None
    
    except Exception as e:
        # If magic fails, we'll allow it but log the issue
        return True, f"Warning: Could not verify file type - {str(e)}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing/replacing dangerous characters."""
    # Remove path components
    filename = os.path.basename(filename)
    
    # Replace dangerous characters with underscores
    filename = re.sub(r'[<>:"|?*\\\/]', '_', filename)
    
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename

def validate_file_upload(uploaded_file) -> Tuple[bool, Optional[str], str]:
    """
    Comprehensive file validation.
    
    Returns:
        (is_valid, error_message, sanitized_filename)
    """
    # Sanitize filename first
    safe_filename = sanitize_filename(uploaded_file.name)
    
    # Validate filename
    valid, error = validate_filename(safe_filename)
    if not valid:
        return False, error, safe_filename
    
    # Validate extension
    valid, error = validate_file_extension(safe_filename)
    if not valid:
        return False, error, safe_filename
    
    # Validate file size
    valid, error = validate_file_size(uploaded_file.size)
    if not valid:
        return False, error, safe_filename
    
    return True, None, safe_filename