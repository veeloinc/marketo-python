import xml.etree.ElementTree as ET
import lead_record


def wrap(email):
    return u"<ns1:paramsGetLead>" \
           u"<leadKey>" \
           u"<keyType>EMAIL</keyType>" \
           u"<keyValue>{email}</keyValue>" \
           u"</leadKey>" \
           u"</ns1:paramsGetLead>".format(email=email)


def unwrap(response):
    root = ET.fromstring(response.text)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
