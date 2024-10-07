import os
from sqlalchemy import create_engine, Column, Integer, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData
from PIL import Image

Base = declarative_base()
DATABASE_URL = 'postgresql+psycopg2://myuser:mypassword@localhost:5432/mydb'  # Example: 'postgresql://user:password@localhost/mydatabase'


# Define the Image model
class ImageModel(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, nullable=False)
    image_data = Column(LargeBinary, nullable=False)


# Function to convert image to binary data
def convert_image_to_binary(image_path):
    with open(image_path, 'rb') as file:
        binary_data = file.read()
    return binary_data


# Function to upload image to the database
def upload_image_to_db(image_path, listing_id):
    # Database connection string (replace with your actual credentials)
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Convert image to binary data
        image_data = convert_image_to_binary(image_path)

        # Create an ImageModel object
        new_image = ImageModel(listing_id=listing_id, image_data=image_data)

        # Add and commit to the session
        session.add(new_image)
        session.commit()
        print(f"Image successfully uploaded with listing ID {listing_id}.")
    except Exception as e:
        session.rollback()
        print(f"Failed to upload image: {e}")
    finally:
        session.close()


# Function to download image from the database
def download_image_from_db(image_id, output_path):
    # Database connection string (replace with your actual credentials)
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Query for the image by ID
        image_entry = session.query(ImageModel).filter_by(id=image_id).first()

        if image_entry:
            # Save the image data to a file
            with open(output_path, 'wb') as file:
                file.write(image_entry.image_data)
            print(f"Image successfully downloaded and saved as {output_path}.")
        else:
            print(f"No image found with ID {image_id}.")
    except Exception as e:
        print(f"Failed to download image: {e}")
    finally:
        session.close()


# Example usage
if __name__ == "__main__":
    # Upload an image
    image_path = "test-img.jpg"  # Replace with the path to your image
    listing_id = 124  # Replace with your listing ID
    upload_image_to_db(image_path, listing_id)

    # Download the same image by ID
    image_id = 1  # Replace with the image ID you want to download
    output_path = "downloaded_image.png"  # Replace with the path where you want to save the downloaded image
    download_image_from_db(image_id, output_path)
