__author__ = 'jeff'

class CampaignRecord:

    def __init__(self):
        self.attributes = {}
        self.description = None
        self.name = None
        self.id = None

    def __str__(self):
        return "Lead (%s - %s)" % (self.id, self.email)

    def __repr__(self):
        return self.__str__()


def unwrap(xml):
    campaign = CampaignRecord()
    campaign.id = int(xml.find('Id').text)

    campaign.name = xml.find('Name').text
    campaign.description = xml.find('Description').text

    for attribute in xml.findall('.//attribute'):
        name = attribute.find('attrName').text
        attr_type = attribute.find('attrType').text
        val = attribute.find('attrValue').text

        if attr_type == 'integer':
            val = int(val)

        campaign.attributes[name] = val

    return campaign
