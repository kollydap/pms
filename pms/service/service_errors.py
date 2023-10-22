import enum
from fastapi import status


class PmsErrorEnum(enum.Enum):
    PMS_001 = ("Account not found", status.HTTP_404_NOT_FOUND)
    PMS_002 = ("Unable to complete update", status.HTTP_400_BAD_REQUEST)
    PMS_003 = ("Unable to complete delete", status.HTTP_400_BAD_REQUEST)
    PMS_004 = ("Employee not found", status.HTTP_404_NOT_FOUND)
    PMS_005 = ("Customer not found", status.HTTP_404_NOT_FOUND)
    PMS_006 = ("Email in use", status.HTTP_400_BAD_REQUEST)
    # PMS_004 = ("")
