from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr


class ResourceCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    company: Optional[str] = None
    alloc_work_hours: Optional[int] = None
    alloc_max_hours: Optional[int] = None
    alloc_night_work: Optional[bool] = None
    alloc_overtime: Optional[bool] = None
    alloc_weekend: Optional[bool] = None
    contact_title: Optional[str] = None
    contact_mobile_phone: Optional[str] = None
    contact_fixed_line: Optional[str] = None
    contact_email: Optional[str] = None
    contact_post_code: Optional[str] = None
    contact_other_info: Optional[str] = None
    contact_street: Optional[str] = None
    contact_city: Optional[str] = None
    contact_province: Optional[str] = None
    contact_country: Optional[str] = None
    last_capacity_date: Optional[date] = None
    last_cost_month: Optional[date] = None
    registration_status: Optional[str] = None
    created_by: str


class ResourceUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    alloc_work_hours: Optional[int] = None
    alloc_max_hours: Optional[int] = None
    alloc_night_work: Optional[bool] = None
    alloc_overtime: Optional[bool] = None
    alloc_weekend: Optional[bool] = None
    contact_title: Optional[str] = None
    contact_mobile_phone: Optional[str] = None
    contact_fixed_line: Optional[str] = None
    contact_email: Optional[str] = None
    contact_post_code: Optional[str] = None
    contact_other_info: Optional[str] = None
    contact_street: Optional[str] = None
    contact_city: Optional[str] = None
    contact_province: Optional[str] = None
    contact_country: Optional[str] = None
    last_capacity_date: Optional[date] = None
    last_cost_month: Optional[date] = None
    registration_status: Optional[str] = None
    updated_by: Optional[str] = None


class ResourceResponse(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    company: Optional[str]
    alloc_work_hours: Optional[int]
    alloc_max_hours: Optional[int]
    alloc_night_work: Optional[bool]
    alloc_overtime: Optional[bool]
    alloc_weekend: Optional[bool]
    contact_title: Optional[str]
    contact_mobile_phone: Optional[str]
    contact_fixed_line: Optional[str]
    contact_email: Optional[str]
    contact_post_code: Optional[str]
    contact_other_info: Optional[str]
    contact_street: Optional[str]
    contact_city: Optional[str]
    contact_province: Optional[str]
    contact_country: Optional[str]
    updated_by: Optional[str]
    date_updated: Optional[str]
    created_by: str
    date_created: str
    last_capacity_date: Optional[str]
    last_cost_month: Optional[str]
    registration_status: Optional[str]
