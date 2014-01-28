import xml.etree.ElementTree as ET
import lead_record


def wrap(email):
    return "<ns1:paramsGetLead>" \
           "<leadKey>" \
           "<keyType>EMAIL</keyType>" \
           "<keyValue>%s</keyValue>" \
           "</leadKey>" \
           "</ns1:paramsGetLead>" % email


def unwrap(response):
    root = ET.fromstring(response.text)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
