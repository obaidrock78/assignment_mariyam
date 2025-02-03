from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session
import uuid
from app.payload_transformer.models import Payload
from app.payload_transformer.request import PayloadCreate
from app.payload_transformer.response import PayloadRead
from app.payload_transformer.utils import (
    compute_hash,
    validate_lists_length,
    get_existing_payload,
    check_and_transform_cache,
    save_cache_entries,
    generate_output_string,
    save_payload,
)
from config.database import get_session

router = APIRouter()


# Endpoints
@router.post("/", response_model=PayloadRead)
def create_payload(payload: PayloadCreate, session: Session = Depends(get_session)):
    validate_lists_length(payload.list_1, payload.list_2)

    # Compute hash to check existing payloads
    hash_value = compute_hash(payload.list_1, payload.list_2)
    existing_payload = get_existing_payload(session, hash_value)
    if existing_payload:
        return existing_payload

    local_cache = {}
    new_cache_entries = []

    def get_transformed(s: str):
        return check_and_transform_cache(s, session, local_cache, new_cache_entries)

    transformed_list1 = [get_transformed(s) for s in payload.list_1]
    transformed_list2 = [get_transformed(s) for s in payload.list_2]

    # Save new cache entries
    save_cache_entries(session, new_cache_entries)

    # Generate output string
    output_str = generate_output_string(transformed_list1, transformed_list2)

    # Save payload to the database
    new_payload = save_payload(session, payload, output_str, hash_value)

    return new_payload


@router.get("/{payload_id}", response_model=PayloadRead)
def read_payload(payload_id: uuid.UUID, session: Session = Depends(get_session)):
    payload = session.get(Payload, payload_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Payload not found")
    return payload
