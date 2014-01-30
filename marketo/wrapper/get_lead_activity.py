import xml.etree.ElementTree as ET
import lead_activity


def wrap(email):
    return u"<ns1:paramsGetLeadActivity>" \
           u"<leadKey>" \
           u"<keyType>EMAIL</keyType>" \
           u"<keyValue>{email}</keyValue>" \
           u"</leadKey>" \
           u"</ns1:paramsGetLeadActivity>".format(email=email)


def unwrap(response):
    root = ET.fromstring(response.text)
    activities = []
    for activity_el in root.findall('.//activityRecord'):
        activity = lead_activity.unwrap(activity_el)
        activities.append(activity)
    return activities
