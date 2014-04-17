import cgi
import xml.etree.ElementTree as ET

import campaign_record


def wrap(source):
    # TODO:       <name>Trigger</name>
    # TODO        <exactName>false</exactName>
    return u"<ns1:paramsGetCampaignsForSource>" \
        u"<source>{source}</source> " \
        u"</ns1:paramsGetCampaignsForSource>".format(source=source)

def unwrap(response):
    root = ET.fromstring(response.content)
    campaign_list = root.findall('.//campaignRecord')
    if campaign_list:
        return [campaign_record.unwrap(campaign) for campaign in campaign_list]
    else:
        return []