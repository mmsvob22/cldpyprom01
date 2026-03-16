from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException

from .database import get_connection
from .models import ResourceCreate, ResourceUpdate, ResourceResponse

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("/", response_model=List[ResourceResponse])
def list_resources():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM Resource ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM Resource WHERE id = ?", (resource_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return dict(row)


@router.post("/", response_model=ResourceResponse, status_code=201)
def create_resource(data: ResourceCreate):
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO Resource (
            first_name, middle_name, last_name, company,
            alloc_work_hours, alloc_max_hours, alloc_night_work, alloc_overtime, alloc_weekend,
            contact_title, contact_mobile_phone, contact_fixed_line, contact_email,
            contact_post_code, contact_other_info, contact_street, contact_city,
            contact_province, contact_country,
            last_capacity_date, last_cost_month, registration_status,
            created_by, date_created
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data.first_name, data.middle_name, data.last_name, data.company,
        data.alloc_work_hours, data.alloc_max_hours,
        int(data.alloc_night_work) if data.alloc_night_work is not None else None,
        int(data.alloc_overtime) if data.alloc_overtime is not None else None,
        int(data.alloc_weekend) if data.alloc_weekend is not None else None,
        data.contact_title, data.contact_mobile_phone, data.contact_fixed_line,
        data.contact_email, data.contact_post_code, data.contact_other_info,
        data.contact_street, data.contact_city, data.contact_province, data.contact_country,
        str(data.last_capacity_date) if data.last_capacity_date else None,
        str(data.last_cost_month) if data.last_cost_month else None,
        data.registration_status, data.created_by, now
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM Resource WHERE id = ?", (cursor.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, data: ResourceUpdate):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM Resource WHERE id = ?", (resource_id,)).fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Resource not found")

    updates = data.model_dump(exclude_none=True)
    updates["date_updated"] = datetime.utcnow().isoformat()

    # convert bool fields to int for SQLite
    for bool_field in ("alloc_night_work", "alloc_overtime", "alloc_weekend"):
        if bool_field in updates:
            updates[bool_field] = int(updates[bool_field])

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [resource_id]
    conn.execute(f"UPDATE Resource SET {set_clause} WHERE id = ?", values)
    conn.commit()
    row = conn.execute("SELECT * FROM Resource WHERE id = ?", (resource_id,)).fetchone()
    conn.close()
    return dict(row)


@router.delete("/{resource_id}", status_code=204)
def delete_resource(resource_id: int):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM Resource WHERE id = ?", (resource_id,)).fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Resource not found")
    conn.execute("DELETE FROM Resource WHERE id = ?", (resource_id,))
    conn.commit()
    conn.close()
