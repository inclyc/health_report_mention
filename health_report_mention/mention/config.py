import pydantic


class Config(pydantic.BaseModel):
    dry_run: bool = True # Try to get data without actually posting
    username: str = "username"
    password: str = "password"
    student_qq_id_path: str = "student_qq_id.csv"