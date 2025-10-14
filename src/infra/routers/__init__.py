from .geography_router import router as geography_router
from .patient_router import router as patient_router
from .psychologist_router import router as psychologist_router
from .session_router import router as session_router
from .user_router import router as user_router

__all__ = [
    "geography_router",
    "patient_router",
    "psychologist_router",
    "session_router",
    "user_router",
]
