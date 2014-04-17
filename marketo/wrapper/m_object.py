__author__ = 'jeff'

class MObject:

    def __init__(self):
        self.attributes = {}

    def __str__(self):
        return "{0} {0}".format(self.object_type, self.id)

    def __repr__(self):
        return self.__str__()


def unwrap(xml):
    mobj = MObject()
    mobj.id = int(xml.find('id').text)
    mobj.object_type = xml.find('type').text

    for attribute in xml.findall('.//attrib'):
        name = attribute.find('name').text
        val = attribute.find('value').text

        mobj.attributes[name] = val

    return mobj
