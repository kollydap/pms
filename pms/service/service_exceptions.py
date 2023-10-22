class NotFoundError(Exception):
    """Something was not found"""


class DeleteError(Exception):
    """Unable to delete"""


class UpdateError(Exception):
    """Unable to update"""


class CreateError(Exception):
    """Unable to create"""


class DuplicateError(Exception):
    """Duplicate Error"""


class InvalidFileType(Exception):
    """File type not supported"""
