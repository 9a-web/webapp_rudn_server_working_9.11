from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import uuid

# --- RUDN Parser Models ---
class Faculty(BaseModel):
    name: str
    id: str
    code: Optional[str] = None  # Optional - not all sources provide this

class FilterOption(BaseModel):
    label: str
    value: Union[str, int]  # Can be string or int (courses come as int)

class FilterDataResponse(BaseModel):
    courses: List[FilterOption] = []
    groups: List[FilterOption] = []
    levels: List[FilterOption] = []
    forms: List[FilterOption] = []

class FilterDataRequest(BaseModel):
    facultet_id: str
    level_id: Optional[str] = None
    kurs: Optional[str] = None
    form_code: Optional[str] = None

class ScheduleRequest(BaseModel):
    group_name: str
    date_start: Optional[str] = None
    date_end: Optional[str] = None

class ScheduleEvent(BaseModel):
    discipline: str
    time: str
    auditory: Optional[str] = None
    teacher: Optional[str] = None
    lesson_type: Optional[str] = None
    date: Optional[str] = None

class ScheduleResponse(BaseModel):
    events: List[ScheduleEvent]

# --- User Settings ---
class UserSettings(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    group_name: Optional[str] = None
    facultet_name: Optional[str] = None
    level: Optional[str] = None
    course: Optional[int] = None
    notifications_enabled: bool = False
    notification_time: int = 15
    referral_code: Optional[str] = None
    referred_by: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserSettingsCreate(UserSettings):
    pass

class UserSettingsResponse(UserSettings):
    pass

# --- Stats & Achievements ---
class UserStats(BaseModel):
    telegram_id: int
    total_points: int = 0
    achievements_count: int = 0
    groups_viewed: int = 0
    friends_invited: int = 0
    schedule_views: int = 0
    tasks_created: int = 0
    calendar_opens: int = 0
    analytics_views: int = 0
    notifications_configured: int = 0
    schedule_shares: int = 0
    menu_items_visited: int = 0
    active_days: int = 0
    night_usage_count: int = 0
    early_usage_count: int = 0
    
class UserStatsResponse(UserStats):
    pass

class Achievement(BaseModel):
    id: str
    name: str
    description: str
    emoji: str
    points: int
    type: str
    requirement: Optional[int] = None

class UserAchievement(BaseModel):
    telegram_id: int
    achievement_id: str
    earned_at: datetime
    seen: bool = False

class UserAchievementResponse(UserAchievement):
    achievement: Achievement

class NewAchievementsResponse(BaseModel):
    new_achievements: List[UserAchievementResponse]

class TrackActionRequest(BaseModel):
    action: str
    data: Optional[Dict[str, Any]] = None

# --- Notifications ---
class NotificationSettingsUpdate(BaseModel):
    enabled: bool
    time: Optional[int] = 15

class NotificationSettingsResponse(BaseModel):
    enabled: bool
    time: int

class NotificationStatsResponse(BaseModel):
    total_sent: int = 0
    success_rate: float = 0.0

class NotificationHistoryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    telegram_id: int
    message: str
    created_at: datetime
    status: str

class NotificationHistoryResponse(BaseModel):
    history: List[NotificationHistoryItem]
    count: int

# --- Tasks ---
class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    telegram_id: int
    text: str
    completed: bool = False
    category: str = "учеба"
    priority: str = "medium"
    deadline: Optional[datetime] = None
    target_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    tags: List[str] = []
    order: int = 0

class TaskCreate(BaseModel):
    text: str
    category: Optional[str] = "учеба"
    priority: Optional[str] = "medium"
    deadline: Optional[datetime] = None
    target_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: List[str] = []

class TaskUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    target_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None

class TaskResponse(Task):
    pass

class TaskProductivityStats(BaseModel):
    total_completed: int
    completed_today: int
    completed_this_week: int
    current_streak: int
    best_streak: int
    daily_stats: List[Dict[str, Any]]

class Subtask(BaseModel):
    id: str
    text: str
    completed: bool

class SubtaskCreate(BaseModel):
    text: str

class SubtaskUpdate(BaseModel):
    completed: bool

class TaskReorderItem(BaseModel):
    id: str
    order: int

class TaskReorderRequest(BaseModel):
    items: List[TaskReorderItem]

# --- Rooms & Group Tasks ---
class Room(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    owner_id: int
    color: str = "blue"
    emoji: str = "🏠"
    created_at: datetime
    total_participants: int = 0
    total_tasks: int = 0
    completed_tasks: int = 0

class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = "blue"
    emoji: Optional[str] = "🏠"
    telegram_id: int

class RoomResponse(Room):
    participants_count: int = 0
    is_owner: bool = False

class RoomParticipant(BaseModel):
    room_id: str
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = "member"
    joined_at: datetime
    referral_code: Optional[int] = None

class RoomInviteLinkResponse(BaseModel):
    link: str
    token: str

class RoomJoinRequest(BaseModel):
    token: str
    telegram_id: int

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    emoji: Optional[str] = None

class ParticipantRoleUpdate(BaseModel):
    role: str

class RoomStatsResponse(BaseModel):
    total_tasks: int
    completed_tasks: int

class RoomActivity(BaseModel):
    room_id: str
    action: str
    user_id: int
    timestamp: datetime

class RoomActivityResponse(BaseModel):
    activities: List[RoomActivity]

class GroupTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    room_id: str
    text: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    deadline: Optional[datetime] = None
    assigned_to: List[int] = []
    category: Optional[str] = None
    tags: List[str] = []
    order: int = 0
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_by: Optional[int] = None
    completed_at: Optional[datetime] = None

class GroupTaskCreate(BaseModel):
    text: str
    room_id: str
    description: Optional[str] = None
    priority: str = "medium"
    deadline: Optional[datetime] = None
    assigned_to: Optional[List[int]] = []
    category: Optional[str] = None
    tags: List[str] = []
    telegram_id: int

class GroupTaskUpdate(BaseModel):
    text: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None
    assigned_to: Optional[List[int]] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class GroupTaskResponse(GroupTask):
    pass

class GroupTaskParticipant(BaseModel):
    user_id: int
    username: Optional[str]

class GroupTaskComment(BaseModel):
    id: str
    task_id: str
    user_id: int
    text: str
    created_at: datetime

class GroupTaskCommentCreate(BaseModel):
    text: str
    telegram_id: int

class GroupTaskCommentResponse(GroupTaskComment):
    pass

class GroupTaskInvite(BaseModel):
    task_id: str
    token: str

class GroupTaskInviteCreate(BaseModel):
    task_id: str

class GroupTaskInviteResponse(GroupTaskInvite):
    pass

class GroupTaskCompleteRequest(BaseModel):
    completed: bool
    telegram_id: int

class RoomTaskCreate(GroupTaskCreate):
    pass

# --- Admin Stats ---
class AdminStatsResponse(BaseModel):
    total_users: int
    active_users_today: int
    total_tasks: int
    total_rooms: int
    total_referrals: int
    total_journal_joins: int = 0
    journal_joins_today: int = 0
    journal_joins_week: int = 0
    total_journals: int = 0

class UserActivityPoint(BaseModel):
    date: str
    count: int

class HourlyActivityPoint(BaseModel):
    hour: int
    count: int

class FeatureUsageStats(BaseModel):
    schedule_views: int
    analytics_views: int
    calendar_opens: int
    notifications_configured: int
    schedule_shares: int
    tasks_created: int
    achievements_earned: int

class TopUser(BaseModel):
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    value: int
    group_name: Optional[str]

class FacultyStats(BaseModel):
    faculty_name: str
    users_count: int
    faculty_id: Optional[str]

class CourseStats(BaseModel):
    course: int
    users_count: int

# --- Referrals ---
class ReferralUser(BaseModel):
    telegram_id: int
    username: Optional[str]
    joined_at: datetime

class ReferralStats(BaseModel):
    total_invited: int
    active_invited: int

class ReferralTreeNode(BaseModel):
    user: ReferralUser
    children: List['ReferralTreeNode'] = []

class ReferralCodeResponse(BaseModel):
    code: str
    link: str

class ReferralConnection(BaseModel):
    referrer_id: int
    referred_id: int
    created_at: datetime

class ProcessReferralRequest(BaseModel):
    referral_code: str
    telegram_id: int

class ProcessReferralResponse(BaseModel):
    success: bool
    message: str

class ReferralEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    telegram_id: int
    referrer_id: Optional[int]
    target_id: str
    target_name: str
    created_at: datetime
    is_new_member: bool = False
    invite_token: Optional[str] = None
    journal_joins: Optional[int] = 0

class ReferralEventResponse(ReferralEvent):
    pass

class ReferralStatsDetailResponse(BaseModel):
    events: List[ReferralEvent]
    total_journal_joins: int
    journal_joins_today: int
    journal_joins_week: int

# --- Journal Models ---
class JournalSettings(BaseModel):
    allow_self_mark: bool = False
    show_group_stats: bool = True
    absence_reasons: List[str] = ["Болезнь", "Уважительная", "Семейные обстоятельства"]

class AttendanceJournal(BaseModel):
    journal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    group_name: str
    description: Optional[str] = None
    owner_id: int
    color: str = "purple"
    invite_token: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    settings: JournalSettings = Field(default_factory=JournalSettings)
    viewer_ids: List[int] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class JournalCreate(BaseModel):
    name: str
    group_name: str
    description: Optional[str] = None
    telegram_id: int
    color: str = "purple"

class JournalResponse(BaseModel):
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

class JournalStudent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    journal_id: str
    full_name: str
    order: int
    telegram_id: Optional[int] = None
    is_linked: bool = False
    invite_code: Optional[str] = None

class JournalStudentCreate(BaseModel):
    full_name: str
    journal_id: Optional[str] = None

class JournalStudentBulkCreate(BaseModel):
    names: List[str]

class JournalStudentLink(BaseModel):
    telegram_id: int

class JournalStudentResponse(JournalStudent):
    pass

class JournalSubject(BaseModel):
    subject_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    journal_id: str
    name: str
    teacher: Optional[str] = None
    
class JournalSubjectCreate(BaseModel):
    name: str
    teacher: Optional[str] = None
    journal_id: Optional[str] = None

class JournalSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    journal_id: str
    subject_id: str
    date: str
    title: str
    description: Optional[str] = None
    type: str = "lecture"
    created_at: datetime
    created_by: int

class JournalSessionCreate(BaseModel):
    subject_id: str
    date: str
    title: str
    description: Optional[str] = None
    type: str = "lecture"
    telegram_id: int
    journal_id: Optional[str] = None

class JournalSessionResponse(JournalSession):
    pass

class ScheduleSessionItem(BaseModel):
    date: str
    time: str
    discipline: str
    lesson_type: str
    teacher: Optional[str] = None
    auditory: Optional[str] = None

class CreateSessionsFromScheduleRequest(BaseModel):
    subject_id: str
    telegram_id: int
    sessions: List[ScheduleSessionItem]

class AttendanceRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    journal_id: str
    session_id: str
    student_id: str
    status: str # present, absent, late, excused
    marked_by: int
    marked_at: datetime

class AttendanceRecordCreate(BaseModel):
    student_id: str
    status: str
    marked_by: int

class AttendanceBulkCreate(BaseModel):
    records: List[AttendanceRecordCreate]

class AttendanceRecordResponse(AttendanceRecord):
    pass

class JournalPendingMember(BaseModel):
    journal_id: str
    telegram_id: int
    full_name: Optional[str] = None
    username: Optional[str] = None
    is_linked: bool = False

class JournalJoinRequest(BaseModel):
    telegram_id: int
    referrer_id: Optional[int] = None

class JoinStudentRequest(BaseModel):
    telegram_id: int

class ProcessJournalInviteRequest(BaseModel):
    invite_code: str
    telegram_id: int
    invite_type: str # journal, jstudent

class JournalStatsResponse(BaseModel):
    journal_id: str
    total_students: int = 0
    linked_students: int = 0
    total_sessions: int = 0
    overall_attendance_percent: float = 0
    students_stats: List[Any] = []
    sessions_stats: List[Any] = []

class JournalInviteLinkResponse(BaseModel):
    invite_link: str
    invite_link_webapp: str
    invite_token: str
    journal_id: str

class StudentInviteLinkResponse(BaseModel):
    invite_link: str
    invite_link_webapp: str
    invite_code: str
    student_id: str

class MyAttendanceResponse(BaseModel):
    attended: int
    total: int
    percent: float

# --- Generic Responses ---
class ErrorResponse(BaseModel):
    detail: str

class SuccessResponse(BaseModel):
    status: str
    message: Optional[str] = None
    
class BotInfo(BaseModel):
    name: str
    version: str

class WeatherResponse(BaseModel):
    temp: float
    description: str
    city: str


class JournalViewerUpdate(BaseModel):
    telegram_id: int
    target_user_id: int
    action: str # "add" or "remove"
