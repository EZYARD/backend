from datetime import datetime
from io import BytesIO
from typing import Optional

import firebase_admin
from fastapi import FastAPI, HTTPException, Depends, Query, Header, Body, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from firebase_admin import auth, credentials
from geopy.distance import geodesic
from googlemaps import Client as GoogleMapsClient
from sqlalchemy import create_engine, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from addTestImages import add_images_to_listings
from constants import DATABASE_URL, MAPS_API_KEY
from images import ImageModel
from listingReturn import ListingModel

app = FastAPI()
gmaps = GoogleMapsClient(key=MAPS_API_KEY)
cred = credentials.Certificate("./serviceKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except firebase_admin.exceptions.FirebaseError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


engine = create_engine(
    DATABASE_URL,
    pool_timeout=30,  # Set pool timeout (in seconds)
    connect_args={"options": "-c statement_timeout=5000"}  # Set statement timeout to 5 seconds (5000 milliseconds)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Endpoint to test the authentication
@app.get("/testAuth")
async def test_auth(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header format")

    token = authorization.split("Bearer ")[1]

    # Verify token and get the user ID
    try:
        user_id = verify_token(token)
        return {"message": "User authenticated", "user_id": user_id}
    except HTTPException as e:
        raise e


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


@app.put("/listings/update/{listing_id}")
async def update_listing(
        listing_id: int,
        name: Optional[str] = Query(None),
        streetNumber: Optional[int] = Query(None),
        streetName: Optional[str] = Query(None),
        city: Optional[str] = Query(None),
        state: Optional[str] = Query(None),
        zipcode: Optional[int] = Query(None),
        description: Optional[str] = Query(None),
        startTime: Optional[datetime] = Query(None),
        endTime: Optional[datetime] = Query(None),
        tags: Optional[str] = Query(None),
        priceRange: Optional[str] = Query(None),
        rating: Optional[str] = Query(None),
        reviews: Optional[str] = Query(None),
        longitude: Optional[float] = Query(None),
        latitude: Optional[float] = Query(None),
        db: Session = Depends(get_db)
):
    # Find the listing by ID
    listing = db.query(ListingModel).filter_by(id=listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    # Prepare an update dictionary with only non-None values
    update_data = {}
    if name is not None:
        update_data['name'] = name
    if streetNumber is not None:
        update_data['streetNumber'] = streetNumber
    if streetName is not None:
        update_data['streetName'] = streetName
    if city is not None:
        update_data['city'] = city
    if state is not None:
        update_data['state'] = state
    if zipcode is not None:
        update_data['zipcode'] = zipcode
    if description is not None:
        update_data['description'] = description
    if startTime is not None:
        update_data['startTime'] = startTime
    if endTime is not None:
        update_data['endTime'] = endTime
    if tags is not None:
        update_data['tags'] = tags
    if priceRange is not None:
        update_data['priceRange'] = priceRange
    if rating is not None:
        update_data['rating'] = rating
    if reviews is not None:
        update_data['reviews'] = reviews
    if longitude is not None:
        update_data['longitude'] = longitude
    if latitude is not None:
        update_data['latitude'] = latitude

    # Perform the update
    if update_data:
        stmt = (
            update(ListingModel)
            .where(ListingModel.id == listing_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        try:
            db.execute(stmt)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error")

    # Fetch the updated listing
    updated_listing = db.query(ListingModel).filter_by(id=listing_id).first()

    return updated_listing


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


# Function to convert an address or zip code to latitude and longitude using Google Maps API
def get_lat_lon_from_address(address: str):
    print("ATTEMPTING TO GET LATITUDE AND LONGITUDE")
    print(address)
    try:
        geocode_result = gmaps.geocode(address)
        if not geocode_result:
            return None

        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error retrieving location information")


# Function to update listings with missing latitude and longitude
def update_missing_coordinates(db: Session):
    listings = db.query(ListingModel).filter(
        (ListingModel.latitude == None) | (ListingModel.longitude == None)).all()

    for listing in listings:
        # Construct the full address of the listing
        listing_address = f"{listing.streetNumber} {listing.streetName}, {listing.city}, {listing.state} {listing.zipcode}"
        location = get_lat_lon_from_address(listing_address)

        if location:
            lat, lng = location
            try:
                # Update the listing with the new coordinates
                stmt = update(ListingModel).where(ListingModel.id == listing.id).values(latitude=lat, longitude=lng)
                db.execute(stmt)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Endpoint to get listings within a given range based on straight-line distance
@app.get("/listings/distance")
async def get_listings_by_distance(
        location: str,
        radius: float,
        db: Session = Depends(get_db)
):
    # Update any listings that are missing coordinates
    update_missing_coordinates(db)

    # Convert the user-provided location to latitude and longitude
    user_location = get_lat_lon_from_address(location)
    if not user_location:
        raise HTTPException(status_code=400, detail="Invalid address or zip code")
    user_lat, user_lng = user_location

    # Retrieve all listings from the database
    listings = db.query(ListingModel).all()

    if not listings:
        raise HTTPException(status_code=404, detail="No listings found")

    # Prepare results list
    results = []

    # Iterate over each listing and calculate the straight-line distance
    for listing in listings:
        if listing.latitude is None or listing.longitude is None:
            continue  # Skip listings that couldn't be updated with coordinates

        listing_location = (listing.latitude, listing.longitude)
        user_location = (user_lat, user_lng)

        # Calculate the straight-line distance in miles
        distance = geodesic(user_location, listing_location).miles

        if distance <= radius:
            results.append({
                "id": listing.id,
                "name": listing.name,
                "address": f"{listing.streetNumber} {listing.streetName}, {listing.city}, {listing.state} {listing.zipcode}",
                "distance_miles": round(distance, 2)
            })

    return results


@app.post("/listings/create")
async def create_listing(
        name: str = Body(...),
        streetNumber: int = Body(...),
        streetName: str = Body(...),
        city: str = Body(...),
        state: str = Body(...),
        zipcode: int = Body(...),
        description: str = Body(...),
        startTime: datetime = Body(...),
        endTime: datetime = Body(...),
        tags: Optional[str] = Body(None),
        priceRange: Optional[str] = Body(None),
        rating: Optional[str] = Body(None),
        reviews: Optional[str] = Body(None),
        longitude: Optional[float] = Body(None),
        latitude: Optional[float] = Body(None),
        db: Session = Depends(get_db),
        authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header format")

    token = authorization.split("Bearer ")[1]
    user_id = verify_token(token)

    # Create a new listing instance
    new_listing = ListingModel(
        uid=user_id,
        name=name,
        streetNumber=streetNumber,
        streetName=streetName,
        city=city,
        state=state,
        zipcode=zipcode,
        description=description,
        startTime=startTime,
        endTime=endTime,
        tags=tags,
        priceRange=priceRange,
        rating=rating,
        reviews=reviews,
        longitude=longitude,
        latitude=latitude
    )

    try:
        db.add(new_listing)
        db.commit()
        db.refresh(new_listing)
        update_missing_coordinates(db)
        #add_images_to_listings()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"message": "Listing created successfully", "listing": new_listing}

@app.post("/images/upload")
async def upload_image(
    listing_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Read the uploaded file's content in binary format
        image_data = await file.read()

        # Save the image to the database using ImageModel
        new_image = ImageModel(listing_id=listing_id, image_data=image_data)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)  # Refresh to get the new image's ID

        return {"message": "Image uploaded successfully", "image_id": new_image.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

