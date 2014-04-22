
import xml.etree.ElementTree as ET
import lead_record


type_attribute_tmpl = u"<attribute>" \
       u"<attrName>{name}</attrName>" \
       u"<attrType>{typ}</attrType>" \
       u"<attrValue>{value}</attrValue>" \
       u"</attribute>"
notype_attribute_tmpl = u"<attribute>" \
       u"<attrName>{name}</attrName>" \
       u"<attrValue>{value}</attrValue>" \
       u"</attribute>"

def _build_attribute(attr):
    if type(attr) == dict:
        if 'typ' in attr:
            tmpl = type_attribute_tmpl
        else:
            tmpl = notype_attribute_tmpl
        return tmpl.format(
            name=attr['name'],
            typ=attr['typ'],
            value=attr['value']
        )
    else:
        if len(attr) == 3:
            return type_attribute_tmpl.format(
                name=attr[0],
                typ=attr[1],
                value=attr[2]
            )
        else:
            return notype_attribute_tmpl.format(
                name=attr[0],
                value=attr[1]
            )

def wrap(email, attributes=()):
    attr = "".join([_build_attribute(attr) for attr in attributes])

    return u"<ns1:paramsSyncLead>" \
           u"<leadRecord>" \
           u"<Email>{email}</Email>" \
           u"<leadAttributeList>{attributes}</leadAttributeList>" \
           u"</leadRecord>" \
           u"<returnLead>true</returnLead>" \
           u"<marketoCookie></marketoCookie>" \
           u"</ns1:paramsSyncLead>".format(email=email, attributes=attr)


def unwrap(response):
    root = ET.fromstring(response.text)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
