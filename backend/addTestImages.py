import os
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import DATABASE_URL
from images import ImageModel  # Assuming these models are in a models.py file
from images import convert_image_to_binary
from listingReturn import ListingModel

# Database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Directory containing test images
TEST_IMAGES_DIR = "test-images"


# Function that checks any listing without images and adds a set of 4 random images from the test-images directory
def add_images_to_listings():
    session = Session()
    try:
        # Get all listings without images
        listings_without_images = (
            session.query(ListingModel)
            .filter(~ListingModel.id.in_(session.query(ImageModel.listing_id)))
            .all()
        )

        if not listings_without_images:
            print("No listings found without images.")
            return

        # Get all image paths from the test-images directory
        all_image_paths = [
            os.path.join(TEST_IMAGES_DIR, img)
            for img in os.listdir(TEST_IMAGES_DIR)
            if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]

        if not all_image_paths:
            print("No images found in the test-images directory.")
            return

        for listing in listings_without_images:
            # Get 4 random images
            selected_images = random.sample(all_image_paths, min(4, len(all_image_paths)))

            for image_path in selected_images:
                # Convert image to binary
                image_data = convert_image_to_binary(image_path)

                # Create and add the image to the database
                new_image = ImageModel(listing_id=listing.id, image_data=image_data)
                session.add(new_image)

        # Commit the changes
        session.commit()
        print(f"Images successfully added to {len(listings_without_images)} listings.")

    except Exception as e:
        session.rollback()
        print(f"Failed to add images to listings: {e}")
    finally:
        session.close()


# Launch script
if __name__ == "__main__":
    add_images_to_listings()
