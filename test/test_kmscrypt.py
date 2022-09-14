import boto3
import base64
import logging

from unittest import TestCase, mock
from moto import mock_kms
from app import encrypt, handler


class TestKMSCrypt(TestCase):

    def setUp(self):
        self.values = ["I like sandwich", "OMG", "It's broken"]

    @mock.patch("app.encrypt")
    def test_encrypt_function_is_not_called(self, mock_encrypt):
        event = context = dict()
        handler(event, context)

        self.assertEqual(mock_encrypt.call_count, 0)

    @mock.patch("app.encrypt")
    def test_encrypt_function_is_called(self, mock_encrypt):
        context = dict()
        handler({"value": self.values[0]}, context)

        self.assertEqual(mock_encrypt.call_count, 1)

    @mock_kms
    @mock.patch('os.getenv')
    def test_encrypt_function_returns_valid_response(self, mock_mockgetenv):
        context = dict()

        mock_kms = boto3.client('kms', region_name='ap-southeast-2')
        mock_key = mock_kms.create_key(Description="Jingle Bells Jingle Bells Jingle Bells")
        mock_key_id = mock_key["KeyMetadata"]["KeyId"]

        mock_mockgetenv.return_value = mock_key_id

        response = handler({"value": self.values[0]}, context)
        keys = response.keys()

        self.assertTrue("key" in keys)
        self.assertEqual(len(keys), 1)
        self.assertIsInstance(response, dict)

    @mock_kms
    @mock.patch('os.getenv')
    def test_kmscrypt_encrypts_values(self, mock_mockgetenv):
        encrypted_values = list()
        decrypted_values = list()

        mock_kms = boto3.client('kms', region_name='ap-southeast-2')
        mock_key = mock_kms.create_key(Description="Jingle Bells Jingle Bells Jingle Bells")
        mock_key_id = mock_key["KeyMetadata"]["KeyId"]

        mock_mockgetenv.return_value = mock_key_id

        for value in self.values:
            encrypted_value = encrypt(value)
            logging.info("Encrypted value: {}".format(encrypted_value))
            encrypted_values.append(encrypted_value)

        self.assertTrue(len(encrypted_values), 3)
        self.assertNotEqual(self.values, encrypted_values)

        for encrypted_value in encrypted_values:
            value = mock_kms.decrypt(CiphertextBlob=base64.b64decode(encrypted_value), KeyId=mock_key_id)
            logging.info("Decrypted value: {}".format(value["Plaintext"].decode("utf-8")))
            decrypted_values.append(value["Plaintext"].decode("utf-8"))

        self.assertTrue(self.values == decrypted_values)
