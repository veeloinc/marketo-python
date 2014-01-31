import cgi
import xml.etree.ElementTree as ET

import lead_record


def wrap(key_type, key_value):
    key_value = cgi.escape(unicode(key_value))
    return u"<ns1:paramsGetLead>" \
           u"<leadKey>" \
           u"<keyType>{key_type}</keyType>" \
           u"<keyValue>{key_value}</keyValue>" \
           u"</leadKey>" \
           u"</ns1:paramsGetLead>".format(key_type=key_type.upper(), key_value=key_value)


def unwrap(response):
    root = ET.fromstring(response)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
