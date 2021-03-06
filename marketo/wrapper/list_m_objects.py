import xml.etree.ElementTree as ET

def wrap():
    return u"<ns1:paramsListMObjects/>"

def unwrap(response):
    root = ET.fromstring(response.content)
    results = root.findall('.//objects')
    return [result.text for result in results]
