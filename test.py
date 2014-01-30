import unittest

from mock import patch

from marketo import auth
from marketo import Client
from marketo.wrapper import get_lead
from marketo.wrapper import get_lead_activity
from marketo.wrapper import sync_lead


class TestAuth(unittest.TestCase):

    def test_header(self):
        user_id = "_user_id_"
        encryption_key = "_encryption_key_"
        timestamp = "_timestamp_"
        signature = "_signature_"

        with patch("marketo.rfc3339.rfc3339", return_value=timestamp):
            with patch("marketo.auth.sign", return_value=signature):
                actual_result = auth.header(user_id, encryption_key)

        expected_result = "<env:Header>" \
                          "<ns1:AuthenticationHeader>" \
                          "<mktowsUserId>%s</mktowsUserId>" \
                          "<requestSignature>%s</requestSignature>" \
                          "<requestTimestamp>%s</requestTimestamp>" \
                          "</ns1:AuthenticationHeader>" \
                          "</env:Header>" % (user_id, signature, timestamp)

        self.assertEqual(actual_result,
                         expected_result)


class TestGetLead(unittest.TestCase):

    def test_get_lead_wrap(self):
        with self.assertRaises(TypeError):
            get_lead.wrap()

        self.assertEqual(get_lead.wrap("john@do.com"),
                         "<ns1:paramsGetLead>"
                         "<leadKey>"
                         "<keyType>EMAIL</keyType>"
                         "<keyValue>john@do.com</keyValue>"
                         "</leadKey>"
                         "</ns1:paramsGetLead>")


class TestGetLeadActivity(unittest.TestCase):

    def test_get_lead_activity_wrap(self):
        with self.assertRaises(TypeError):
            get_lead_activity.wrap()

        self.assertEqual(get_lead_activity.wrap("john@do.com"),
                         "<ns1:paramsGetLeadActivity>"
                         "<leadKey>"
                         "<keyType>EMAIL</keyType>"
                         "<keyValue>john@do.com</keyValue>"
                         "</leadKey>"
                         "</ns1:paramsGetLeadActivity>")


class TestSyncLead(unittest.TestCase):

    def test_sync_lead_wrap(self):
        with self.assertRaises(TypeError):
            sync_lead.wrap()

        # with empty attribute set
        self.assertEqual(sync_lead.wrap(email="john@do.com", attributes=()),
                         "<mkt:paramsSyncLead>"
                         "<leadRecord>"
                         "<Email>john@do.com</Email>"
                         "<leadAttributeList></leadAttributeList>"
                         "</leadRecord>"
                         "<returnLead>true</returnLead>"
                         "<marketoCookie></marketoCookie>"
                         "</mkt:paramsSyncLead>")

        # with 1 attribute
        self.assertEqual(sync_lead.wrap(email="john@do.com", attributes=(("Name", "string", "John Do"),)),
                         "<mkt:paramsSyncLead>"
                         "<leadRecord>"
                         "<Email>john@do.com</Email>"
                         "<leadAttributeList>"
                         "<attribute>"
                         "<attrName>Name</attrName>"
                         "<attrType>string</attrType>"
                         "<attrValue>John Do</attrValue>"
                         "</attribute>"
                         "</leadAttributeList>"
                         "</leadRecord>"
                         "<returnLead>true</returnLead>"
                         "<marketoCookie></marketoCookie>"
                         "</mkt:paramsSyncLead>")

        # with more attributes
        self.assertEqual(sync_lead.wrap(email="john@do.com", attributes=(("Name", "string", "John Do"),
                                                                         ("Age", "integer", "20"),)),
                         "<mkt:paramsSyncLead>"
                         "<leadRecord>"
                         "<Email>john@do.com</Email>"
                         "<leadAttributeList>"
                         "<attribute>"
                         "<attrName>Name</attrName>"
                         "<attrType>string</attrType>"
                         "<attrValue>John Do</attrValue>"
                         "</attribute>"
                         "<attribute>"
                         "<attrName>Age</attrName>"
                         "<attrType>integer</attrType>"
                         "<attrValue>20</attrValue>"
                         "</attribute>"
                         "</leadAttributeList>"
                         "</leadRecord>"
                         "<returnLead>true</returnLead>"
                         "<marketoCookie></marketoCookie>"
                         "</mkt:paramsSyncLead>")


class TestClient(unittest.TestCase):

    def test_wrap(self):
        soap_endpoint = "_soap_endpoint_"
        user_id = "_user_id_"
        encryption_key = "_encryption_key_"
        client = Client(soap_endpoint=soap_endpoint, user_id=user_id, encryption_key=encryption_key)
        body = "<body/>"
        header = "<header/>"

        with patch("marketo.auth.header", return_value=header):
            actual_result = client.wrap(body=body)

        self.assertEqual(actual_result,
                         '<?xml version="1.0" encoding="UTF-8"?>'
                         '<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
                         'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                         'xmlns:wsdl="http://www.marketo.com/mktows/" '
                         'xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" '
                         'xmlns:ins0="http://www.marketo.com/mktows/" '
                         'xmlns:ns1="http://www.marketo.com/mktows/" '
                         'xmlns:mkt="http://www.marketo.com/mktows/">'
                         '%s'
                         '<env:Body>'
                         '%s'
                         '</env:Body>'
                         '</env:Envelope>' % (header, body))


if __name__ == '__main__':
    unittest.main()
