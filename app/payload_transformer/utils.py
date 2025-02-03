from typing import List
import json
import hashlib

from fastapi import HTTPException
from sqlmodel import Session, select

from app.payload_transformer.models import Payload, TransformerCache
from app.payload_transformer.request import PayloadCreate


def compute_hash(list_1: List[str], list_2: List[str]) -> str:
    data = {"list_1": list_1, "list_2": list_2}
    serialized = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def validate_lists_length(list_1, list_2):
    if len(list_1) != len(list_2):
        raise HTTPException(status_code=400, detail="Lists must be of the same length")


def save_payload(
    session: Session, payload: PayloadCreate, output_str: str, hash_value: str
):
    new_payload = Payload(
        hash=hash_value, list_1=payload.list_1, list_2=payload.list_2, output=output_str
    )
    session.add(new_payload)
    session.commit()
    session.refresh(new_payload)
    return new_payload


def generate_output_string(list1, list2):
    output_parts = []
    for t1, t2 in zip(list1, list2):
        output_parts.extend([t1, t2])
    return ", ".join(output_parts)


def save_cache_entries(session: Session, new_cache_entries: list):
    if new_cache_entries:
        session.bulk_save_objects(new_cache_entries)
        session.commit()


def get_existing_payload(session: Session, hash_value: str):
    return session.exec(
        select(Payload).where(Payload.hash == hash_value) # noqa
    ).first()


def check_and_transform_cache(
    s: str, session: Session, local_cache: dict, new_cache_entries: list
):
    # Check database
    cached_db = session.exec(
        select(TransformerCache).where(TransformerCache.original_string == s) # noqa
    ).first()
    if cached_db:
        local_cache[s] = cached_db.transformed_string
        return cached_db.transformed_string

    # Check local cache
    if s in local_cache:
        return local_cache[s]

    # Transform and cache
    transformed = s.upper()
    local_cache[s] = transformed
    new_cache_entries.append(
        TransformerCache(original_string=s, transformed_string=transformed)
    )
    return transformed
