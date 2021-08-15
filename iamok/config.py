from pydantic import BaseSettings


class Config(BaseSettings):

    iamok_sqlite_path: str
    iamok_report_time_hr: str = "12"
    iamok_report_time_min: str = "0"
    iamok_msg_type: str = "private"
    iamok_id: int

    class Config:
        extra = "ignore"
        