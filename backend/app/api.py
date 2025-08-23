from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.config.services import Services
from app.schemas import LostItemInput
from app.config.services import get_services

router = APIRouter()

@router.post("/submit_found_item")
async def submit_found_item(
    image: UploadFile = File(...),
    location: str = "unknown",
    services: Services = Depends(get_services),
):
    try:
        image_bytes = await image.read()

        # Upload image
        image_url = await services.storage_service.upload_image(image_bytes, image.filename)

        # Insert metadata to Postgres
        item_data = {
            "type": "found",
            "description": None,
            "image_url": image_url,
            "location": location
        }
        item_id = await services.db_service.insert_item(item_data)

        # Generate image embedding
        result = services.image_service.process_found_image(image_bytes)
        embedding = result["embedding"]

        # Insert into Qdrant
        await services.vector_service.insert_item_vector(item_id, embedding, {
            "type": "found",
            "image_url": image_url,
            "location": location
        })

        # Search for similar lost items
        matches = await services.vector_service.search_similar(
            vector=embedding,
            top_k=5,
            filter_payload={"type": "lost"}
        )

        # Store matches
        match_records = [
            {
                "found_item_id": item_id,
                "lost_item_id": m["id"],
                "score": m["score"]
            }
            for m in matches
        ]
        await services.db_service.insert_matches(match_records)

        return {
            "item_id": item_id,
            "image_url": image_url,
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
        # Insert lost item into Postgres
        item_data = {
            "type": "lost",
            "description": item.description,
            "image_url": None,
            "location": item.location
        }
        item_id = await services.db_service.insert_item(item_data)

        # Generate embedding
        embedding = services.text_service.embed_text(item.description)

        # Insert into Qdrant
        await services.vector_service.insert_item_vector(item_id, embedding, {
            "type": "lost",
            "location": item.location
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
                "lost_item_id": item_id,
                "found_item_id": match["id"],
                "score": match["score"]
            }
            for match in matches
        ]
        await services.db_service.insert_matches(match_records)

        return {
            "item_id": item_id,
            "matches": matches
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))