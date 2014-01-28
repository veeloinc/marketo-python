
import unittest

import marketo
import marketo.auth
from marketo.wrapper import get_lead
from marketo.wrapper import get_lead_activity
from marketo.wrapper import sync_lead


class MarketoBasicTests(unittest.TestCase):

    def test_auth(self):
        # From Marketo example"
        user_id = "bigcorp1_461839624B16E06BA2D663"
        encryption_key = "899756834129871744AAEE88DDCC77CDEEDEC1AAAD66"
        timestamp = "2010-04-09T14:04:54-07:00"
        signature = "ffbff4d4bef354807481e66dc7540f7890523a87"
        self.assertTrue(marketo.auth.sign(timestamp + user_id, encryption_key) == signature)


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


if __name__ == '__main__':
    unittest.main()
