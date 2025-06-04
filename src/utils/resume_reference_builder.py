import re
from datetime import datetime, timezone

from models import ResumeReference


def build_resume_reference(resume_id: str, full_name: str) -> ResumeReference:
    filename = generate_resume_filename(full_name)
    return ResumeReference(
        id=resume_id,
        filename=filename,
        created_at=datetime.now(timezone.utc).isoformat()
    )

def generate_resume_filename(full_name: str, suffix: str = "", extension: str = ".pdf") -> str:
    name_parts = re.sub(r"[^a-zA-Z0-9]", "_", full_name.strip().lower()).split("_")
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else "unknown"
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{first_name}_{last_name}_resume_{date_str}{suffix}{extension}"
    return filename