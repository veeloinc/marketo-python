__author__ = 'jeff'

class CampaignRecord:

    def __init__(self):
        self.description = None
        self.name = None
        self.id = None

    def __str__(self):
        return "Campaign {0}".format(self.name)

    def __repr__(self):
        return self.__str__()


def unwrap(xml):
    campaign = CampaignRecord()
    campaign.id = int(xml.find('id').text)

    campaign.name = xml.find('name').text
    campaign.description = xml.find('description').text

    return campaign
