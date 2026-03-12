class AppError(Exception):
    """Excepción base de la aplicación."""


class PermissionDeniedError(AppError):
    """Error para denegar acciones por permisos insuficientes."""
