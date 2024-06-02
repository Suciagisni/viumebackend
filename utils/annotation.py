from pymongo import MongoClient
from bcrypt import hashpw, gensalt, checkpw
import datetime
from email_validator import validate_email, EmailNotValidError
from config.db import db
from bson import ObjectId

annotation = db['annotation']


# get annotation with imageId
def get_annotation(imageId):
    result = annotation.find_one({'imageId':  imageId})
    if result:
        sanitized_result = {
            "_id": str(result["_id"]),
            "imageId": result["imageId"],
            "listAnnotation": result["listAnnotation"],
        }
        return sanitized_result
    else:
        return None

# update annotation with imageId
def update_annotation(imageId, listAnnotation):

    result = get_annotation(imageId)
    if not result:
        annotation.insert_one({"imageId": imageId, "listAnnotation": listAnnotation})
    else:
        annotation.update_one({'imageId': imageId}, {"$set": {"listAnnotation": listAnnotation}})
    
    return True


def add_annotation(imageId, listAnnotation):
    result = annotation.find_one({"imageId": imageId})
    if not result:
        annotation.insert_one({"imageId": imageId, "listAnnotation": listAnnotation})
    else:
        annotation.update_one({'imageId': imageId}, {"$push": {"listAnnotation": {"$each": listAnnotation}}})

    return True

def convert_to_yolo_format(input_string, image_width, image_height, tag):
    # Split the input string by commas and extract the values
    values = input_string.split(':')[-1].split(',')
    
    # Extract the pixel coordinates from the values
    x_pixel = float(values[0])
    y_pixel = float(values[1])
    w_pixel = float(values[2])
    h_pixel = float(values[3])

    # Normalize the coordinates
    x_normalized = x_pixel / image_width
    y_normalized = y_pixel / image_height
    w_normalized = w_pixel / image_width
    h_normalized = h_pixel / image_height

    # Calculate the center point of the bounding box
    x_center = x_normalized + (w_normalized / 2)
    y_center = y_normalized + (h_normalized / 2)

    # Create the YOLO format string with consistent formatting
    yolo_string = f"{tag} {x_center:.12f} {y_center:.12f} {w_normalized:.12f} {h_normalized:.12f}"

    return yolo_string





# get all annotation with imageId and convert to yolo format
def get_annotation_yolo(imageId, image_width, image_height):
   
    result = get_annotation(imageId)
    if result:
        listAnnotation = result["listAnnotation"]
        abnormal = []
        normal = []
        other = []
        for annotation in listAnnotation:
            selector = annotation['target']['selector']['type']
            if selector == "FragmentSelector":
                for list_body in annotation['body']:
                    if list_body['purpose'] == "tagging":
                        tag = list_body['value']
                        annotation_yolo = convert_to_yolo_format(annotation['target']['selector']['value'], image_width, image_height, tag)

                        if "predict" in tag:
                            continue

                        if tag == "abnormal":
                            abnormal.append(annotation_yolo)
                        elif tag == "normal":
                            normal.append(annotation_yolo)
                        else:
                            other.append(annotation_yolo)

        return {"abnormal": abnormal, "normal": normal, "other": other}
    else:
        return None