
import xml.etree.ElementTree as ET
import lead_record


def wrap(email, attributes=()):
    tmpl = u"<attribute>" \
           u"<attrName>{name}</attrName>" \
           u"<attrType>{typ}</attrType>" \
           u"<attrValue>{value}</attrValue>" \
           u"</attribute>"
    attr = "".join(tmpl.format(name=name, typ=typ, value=value) for name, typ, value in attributes)

    return u"<mkt:paramsSyncLead>" \
           u"<leadRecord>" \
           u"<Email>{email}</Email>" \
           u"<leadAttributeList>{attributes}</leadAttributeList>" \
           u"</leadRecord>" \
           u"<returnLead>true</returnLead>" \
           u"<marketoCookie></marketoCookie>" \
           u"</mkt:paramsSyncLead>".format(email=email, attributes=attr)


def unwrap(response):
    root = ET.fromstring(response.text)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
