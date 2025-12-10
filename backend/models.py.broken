class JournalResponse(BaseModel):
    """Ответ с журналом"""
    journal_id: str
    name: str
    group_name: str
    description: Optional[str]
    owner_id: int
    color: str
    invite_token: str
    settings: JournalSettings
    created_at: datetime
    updated_at: datetime
    total_students: int = 0
    linked_students: int = 0
    total_sessions: int = 0
    is_owner: bool = False
    my_attendance_percent: Optional[float] = None
    viewer_ids: List[int] = []
    viewer_ids: List[int] = []  # Список пользователей с доступом к статистике
