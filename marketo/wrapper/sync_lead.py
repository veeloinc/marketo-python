
import xml.etree.ElementTree as ET
import lead_record


def wrap(email, attributes=()):
    tmpl = "<attribute>" \
           "<attrName>%s</attrName>" \
           "<attrType>%s</attrType>" \
           "<attrValue>%s</attrValue>" \
           "</attribute>"
    attr = "".join(tmpl % (name, typ, value) for name, typ, value in attributes)

    return "<mkt:paramsSyncLead>" \
           "<leadRecord>" \
           "<Email>%s</Email>" \
           "<leadAttributeList>%s</leadAttributeList>" \
           "</leadRecord>" \
           "<returnLead>true</returnLead>" \
           "<marketoCookie></marketoCookie>" \
           "</mkt:paramsSyncLead>" % (email, attr)


def unwrap(response):
    root = ET.fromstring(response.text)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
