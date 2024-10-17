from io import BytesIO

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from constants import DATABASE_URL
from images import ImageModel
from listingReturn import ListingModel

app = FastAPI()

engine = create_engine(
    DATABASE_URL,
    pool_timeout=30,  # Set pool timeout (in seconds)
    connect_args={"options": "-c statement_timeout=5000"}  # Set statement timeout to 5 seconds (5000 milliseconds)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Helper function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Route to return metadata of images by listing_id
@app.get("/images/{listing_id}")
async def get_images_by_listing(listing_id: int, db: Session = Depends(get_db)):
    # Query the database for all images with the given listing_id
    images = db.query(ImageModel).filter_by(listing_id=listing_id).all()

    if not images:
        raise HTTPException(status_code=404, detail="No images found for the listing ID")

    # Return metadata about the images (e.g., their IDs and download URLs)
    return [{"id": image.id, "download_url": f"/images/download/{image.id}"} for image in images]


async def iterfile(image_data):
    yield image_data.read()


@app.get("/images/download/{image_id}")
async def download_image(image_id: int, db: Session = Depends(get_db)):
    # Query the database for the image by its ID
    image = db.query(ImageModel).filter_by(id=image_id).first()

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # Convert the binary data to a file-like object using BytesIO
    image_data = BytesIO(image.image_data)

    # Return the image as a streaming response with proper chunking
    return StreamingResponse(iterfile(image_data), media_type="image/png")  # Adjust media type as needed


# Route to return metadata of images by listing_id
@app.get("/listings")
async def get_images_by_listing(db: Session = Depends(get_db)):
    # Query the database for all images with the given listing_id
    listings = db.query(ListingModel).all()

    if not listings:
        raise HTTPException(status_code=404, detail="No listings found for the listing ID")

    # Return metadata about the images (e.g., their IDs and download URLs)
    return listings
