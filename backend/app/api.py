from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from app.config.services import Services, get_services
from app.schemas import LostItemInput
from typing import List

router = APIRouter()

@router.post("/submit_found_item")
async def submit_found_item(
    image: UploadFile = File(...),
    location_hint: str = Form("unknown"),
    services: Services = Depends(get_services),
):
    try:
        image_bytes = await image.read()
        defaut_bucket = "found_item_images"

        # Upload image
        image_filename = image.filename or "uploaded_image.jpg"
        path = await services.storage_service.upload_image(image_bytes, image_filename)

        # Insert metadata to Postgres
        item_data = {
            "image_bucket": defaut_bucket,
            "image_path": path,
            "caption_text": "",  # fill in after model caption if needed
            "location_hint": location_hint
        }
        found_item_id = await services.db_service.insert_found_item(item_data)

        # Generate image embedding
        result = await services.image_service.process_found_image(image_bytes)
        embedding: List[float] = result["embedding"]

        # Insert into Qdrant
        await services.vector_service.insert_item_vector(found_item_id, embedding, {
            "type": "found",
            "image_bucket": defaut_bucket,
            "image_path": path,
            "location_hint": location_hint
        })

        # Search for similar lost items
        matches = await services.vector_service.search_similar(
            vector=embedding,
            top_k=5,
            filter_payload={"type": "lost"}
        )

        # Store matches in Postgres
        match_records = [
            {
                "found_item_id": found_item_id,
                "lost_report_id": m["id"],   # matches Qdrant payload id
                "score": m["score"]
            }
            for m in matches
        ]
        # await services.db_service.insert_matches(match_records)

        return {
            "found_item_id": found_item_id,
            "image_bucket": defaut_bucket,
            "image_path": path,
            "top_matches": matches
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit_lost_item")
async def submit_lost_item(
    item: LostItemInput,
    services: Services = Depends(get_services),
):
    try:
        # Insert lost report into Postgres
        item_data = {
            "description_text": item.description,
            "location_hint": item.location_hint
        }
        lost_report_id = await services.db_service.insert_lost_report(item_data)

        # Generate embedding from text
        embedding = await services.text_service.embed_text(item.description)

        # Insert into Qdrant
        await services.vector_service.insert_item_vector(lost_report_id, embedding, {
            "type": "lost",
            "location_hint": item.location_hint
        })

        # Query for similar found items
        matches = await services.vector_service.search_similar(
            vector=embedding,
            top_k=5,
            filter_payload={"type": "found"}
        )

        # Store match records
        match_records = [
            {
                "lost_report_id": lost_report_id,
                "found_item_id": match["id"],
                "score": match["score"]
            }
            for match in matches
        ]
        await services.db_service.insert_matches(match_records)

        return {
            "lost_report_id": lost_report_id,
            "matches": matches
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
