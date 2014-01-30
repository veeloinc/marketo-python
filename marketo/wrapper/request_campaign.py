
def wrap(campaign, lead):
    return u'<mkt:paramsRequestCampaign>' \
           u'<source>MKTOWS</source>' \
           u'<campaignId>{campaign}</campaignId>' \
           u'<leadList>' \
           u'<leadKey>' \
           u'<keyType>IDNUM</keyType>' \
           u'<keyValue>{lead}</keyValue>' \
           u'</leadKey>' \
           u'</leadList>' \
           u'</mkt:paramsRequestCampaign>'.format(campaign=campaign, lead=lead)
