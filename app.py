import os
import boto3
import logging
import base64

logging.getLogger(__name__)


def encrypt(text):
    kms_id = os.getenv("KMSKEYID")
    kms = boto3.client('kms', region_name='ap-southeast-2')
    ciphertext = kms.encrypt(KeyId=kms_id, Plaintext=text.encode('utf-8'))
    return base64.b64encode(ciphertext["CiphertextBlob"])


def handler(event, context):
    response = dict()
    try:
        text = event.get("value")

        if text:
            response["key"] = encrypt(text)
            return response

    except Exception as ex:
        error_msg = "{}".format(ex)
        logging.error(error_msg)
        return {"statusCode": 400, "error": error_msg}
