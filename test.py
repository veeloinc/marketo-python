# -*- coding: utf-8 -*-
import unittest

from mock import patch

from marketo import auth
from marketo import Client
from marketo.wrapper import exceptions
from marketo.wrapper import get_lead
from marketo.wrapper import get_lead_activity
from marketo.wrapper import request_campaign
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


class TestExceptionParser(unittest.TestCase):

    def test_non_xml_message(self):
        exception_message = 'Non XML message'
        exception_instance = exceptions.unwrap(exception_message)

        self.assertTrue(isinstance(exception_instance, exceptions.MktException))
        self.assertEqual(exception_instance.args, ("Marketo exception message parsing error: %s" % exception_message, ))

    def test_fault_with_details(self):
        exception_message = '<?xml version="1.0" encoding="UTF-8"?>' \
                            '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">' \
                            '<SOAP-ENV:Body>' \
                            '<SOAP-ENV:Fault>' \
                            '<faultcode>SOAP-ENV:Client</faultcode>' \
                            '<faultstring>20103 - Lead not found</faultstring>' \
                            '<detail>' \
                            '<ns1:serviceException xmlns:ns1="http://www.marketo.com/mktows/">' \
                            '<name>mktServiceException</name>' \
                            '<message>No lead found with EMAIL = john@do.com (20103)</message>' \
                            '<code>20103</code>' \
                            '</ns1:serviceException>' \
                            '</detail>' \
                            '</SOAP-ENV:Fault>' \
                            '</SOAP-ENV:Body>' \
                            '</SOAP-ENV:Envelope>'
        exception_instance = exceptions.unwrap(exception_message)

        self.assertTrue(isinstance(exception_instance, exceptions.MktLeadNotFound))
        self.assertEqual(exception_instance.args, ("No lead found with EMAIL = john@do.com (20103)", ))

    def test_fault_without_details(self):
        exception_message = '<?xml version="1.0" encoding="UTF-8"?>' \
                            '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">' \
                            '<SOAP-ENV:Body>' \
                            '<SOAP-ENV:Fault>' \
                            '<faultcode>SOAP-ENV:Client</faultcode>' \
                            '<faultstring>Bad Request</faultstring>' \
                            '</SOAP-ENV:Fault>' \
                            '</SOAP-ENV:Body>' \
                            '</SOAP-ENV:Envelope>'
        exception_instance = exceptions.unwrap(exception_message)

        self.assertTrue(isinstance(exception_instance, exceptions.MktException))
        self.assertEqual(exception_instance.args, ("Bad Request", ))


class TestGetLead(unittest.TestCase):

    def test_get_lead_wrap(self):
        self.assertEqual(get_lead.wrap("john@do.com"),
                         u"<ns1:paramsGetLead>"
                         u"<leadKey>"
                         u"<keyType>EMAIL</keyType>"
                         u"<keyValue>john@do.com</keyValue>"
                         u"</leadKey>"
                         u"</ns1:paramsGetLead>")


class TestGetLeadActivity(unittest.TestCase):

    def test_get_lead_activity_wrap(self):
        self.assertEqual(get_lead_activity.wrap("john@do.com"),
                         u"<ns1:paramsGetLeadActivity>"
                         u"<leadKey>"
                         u"<keyType>EMAIL</keyType>"
                         u"<keyValue>john@do.com</keyValue>"
                         u"</leadKey>"
                         u"</ns1:paramsGetLeadActivity>")


class TestRequestCampaign(unittest.TestCase):

    def test_request_campaign_wrap(self):
        self.assertEqual(request_campaign.wrap(campaign=1, lead='2'),
                         u'<mkt:paramsRequestCampaign>'
                         u'<source>MKTOWS</source>'
                         u'<campaignId>1</campaignId>'
                         u'<leadList>'
                         u'<leadKey>'
                         u'<keyType>IDNUM</keyType>'
                         u'<keyValue>2</keyValue>'
                         u'</leadKey>'
                         u'</leadList>'
                         u'</mkt:paramsRequestCampaign>')


class TestSyncLead(unittest.TestCase):

    def test_sync_lead_wrap(self):
        # with empty attribute set
        self.assertEqual(sync_lead.wrap(email="john@do.com", attributes=()),
                         u"<mkt:paramsSyncLead>"
                         u"<leadRecord>"
                         u"<Email>john@do.com</Email>"
                         u"<leadAttributeList></leadAttributeList>"
                         u"</leadRecord>"
                         u"<returnLead>true</returnLead>"
                         u"<marketoCookie></marketoCookie>"
                         u"</mkt:paramsSyncLead>")

        # with 1 attribute
        self.assertEqual(sync_lead.wrap(email="john@do.com", attributes=(("Name", "string", u"John Do, a hős"),)),
                         u"<mkt:paramsSyncLead>"
                         u"<leadRecord>"
                         u"<Email>john@do.com</Email>"
                         u"<leadAttributeList>"
                         u"<attribute>"
                         u"<attrName>Name</attrName>"
                         u"<attrType>string</attrType>"
                         u"<attrValue>John Do, a hős</attrValue>"
                         u"</attribute>"
                         u"</leadAttributeList>"
                         u"</leadRecord>"
                         u"<returnLead>true</returnLead>"
                         u"<marketoCookie></marketoCookie>"
                         u"</mkt:paramsSyncLead>")

        # with more attributes
        self.assertEqual(sync_lead.wrap(email="john@do.com", attributes=(("Name", "string", "John Do"),
                                                                         ("Age", "integer", "20"),)),
                         u"<mkt:paramsSyncLead>"
                         u"<leadRecord>"
                         u"<Email>john@do.com</Email>"
                         u"<leadAttributeList>"
                         u"<attribute>"
                         u"<attrName>Name</attrName>"
                         u"<attrType>string</attrType>"
                         u"<attrValue>John Do</attrValue>"
                         u"</attribute>"
                         u"<attribute>"
                         u"<attrName>Age</attrName>"
                         u"<attrType>integer</attrType>"
                         u"<attrValue>20</attrValue>"
                         u"</attribute>"
                         u"</leadAttributeList>"
                         u"</leadRecord>"
                         u"<returnLead>true</returnLead>"
                         u"<marketoCookie></marketoCookie>"
                         u"</mkt:paramsSyncLead>")


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
                         u'<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
                         u'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                         u'xmlns:wsdl="http://www.marketo.com/mktows/" '
                         u'xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" '
                         u'xmlns:ins0="http://www.marketo.com/mktows/" '
                         u'xmlns:ns1="http://www.marketo.com/mktows/" '
                         u'xmlns:mkt="http://www.marketo.com/mktows/">'
                         u'{header}'
                         u'<env:Body>'
                         u'{body}'
                         u'</env:Body>'
                         u'</env:Envelope>'.format(header=header, body=body))


if __name__ == '__main__':
    unittest.main()
