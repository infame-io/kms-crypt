import os
import boto3
import logging
import base64

KMS_ID = os.getenv("KMS_ID")

logger = logging.getLogger("kms_crypt")


def encrypt(text):
    kms = boto3.client('kms')

    ciphertext = kms.encrypt(KeyId=KMS_ID, Plaintext=text.encode('utf-8'))

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
        logger.error(error_msg)
        return {"statusCode": 400, "error": error_msg}
