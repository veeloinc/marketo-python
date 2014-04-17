__author__ = 'jeff'

import xml.etree.ElementTree as ET
import m_object

def wrap(object_type):
    return u"   <ns1:paramsGetMObjects>"\
        u"<type>{object_type}</type>"\
        u"</ns1:paramsGetMObjects>".format(
        object_type=object_type
    )

def unwrap(response):
    root = ET.fromstring(response.content)
    results = root.findall('.//mObject')
    return [m_object.unwrap(result) for result in results]
