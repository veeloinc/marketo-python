
import version

VERSION = version.VERSION
__version__ = VERSION

import requests
import auth

from marketo.wrapper import exceptions
from marketo.wrapper import (
    get_lead, get_lead_activity, sync_lead,
    get_campaigns_for_source, request_campaign,
    list_m_objects, get_m_objects,
)


class Client:

    def __init__(self, soap_endpoint, user_id, encryption_key):
        self.soap_endpoint = soap_endpoint
        self.user_id = user_id
        self.encryption_key = encryption_key

    def wrap(self, body):
        payload = u'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" '\
                u'xmlns:ns1="http://www.marketo.com/mktows/"> ' \
                u'<SOAP-ENV:Header> ' \
                u'{header} ' \
                u'</SOAP-ENV:Header> ' \
                u'<SOAP-ENV:Body> ' \
                u'{body} ' \
                u'</SOAP-ENV:Body> ' \
	            u'</SOAP-ENV:Envelope> '.format(
                    header=auth.header(self.user_id, self.encryption_key),
                    body=body
        )
        return payload

    def request(self, body):
        envelope = self.wrap(body).encode("utf-8")
        data = '<?xml version="1.0" encoding="UTF-8"?>' \
               '{envelope}'.format(envelope=envelope)
        response = requests.post(self.soap_endpoint,
                                 data=data,
                                 headers={'Connection': 'Keep-Alive',
                                          'Soapaction': '',
                                          'Content-Type': 'text/xml;charset=UTF-8',
                                          'Accept': '*/*'})
        return response

    def get_lead(self, idnum=None, cookie=None, email=None, sfdcleadid=None, leadowneremail=None,
                 sfdcaccountid=None, sfdccontactid=None, sfdcleadownerid=None, sfdcopptyid=None, **kwargs):
        """
        This function retrieves a single lead record from Marketo.
        If the lead exists based on the input parameters, the lead record attributes will be returned in the result.
        http://developers.marketo.com/documentation/soap/getlead/

        :param idnum: The Marketo ID
        :param cookie: The value generated by the Munchkin Javascript
        :param email: The email address associated with the lead
        :param sfdcleadid: The lead ID from SalesForce
        :param leadowneremail: The Lead Owner Email
        :param sfdcaccountid: The Account ID from SalesForce
        :param sfdccontactid: The Contact ID from SalesForce
        :param sfdcleadownerid: The Lead owner ID from SalesForce
        :param sfdcopptyid: The Opportunity ID from SalesForce
        :param kwargs: For other keytypes in the future...
        :return: :raise exceptions.unwrap:
        """
        # collect all keyword arguments
        key_types = locals().copy()
        del key_types["self"]
        del key_types["kwargs"]
        key_types.update(kwargs)
        for each in key_types.keys():
            if not key_types[each]:
                del key_types[each]

        if len(key_types) != 1:
            raise exceptions.MktException("get_leads() takes exactly 1 keyword argument (%d given)" % len(key_types))

        body = get_lead.wrap(*(key_types.items()[0]))

        response = self.request(body)

        if response.status_code == 200:
            return get_lead.unwrap(response.text.encode("utf-8"))
        else:
            raise exceptions.unwrap(response.text)

    def get_lead_activity(self, email=None):

        if not email or not isinstance(email, (str, unicode)):
            raise ValueError('Must supply an email as a non empty string.')

        body = get_lead_activity.wrap(email)
        response = self.request(body)
        if response.status_code == 200:
            return get_lead_activity.unwrap(response)
        else:
            raise Exception(response.text)

    def get_campaigns_for_source(self, source='MKTOWS'):
        body = get_campaigns_for_source.wrap(source)

        response = self.request(body)
        if response.status_code == 200:
            return get_campaigns_for_source.unwrap(response)
        else:
            raise Exception(response.text)

    def get_m_objects(self, object_type='Program'):
        body = get_m_objects.wrap(object_type)

        response = self.request(body)
        if response.status_code == 200:
            return get_m_objects.unwrap(response)
        else:
            raise Exception(response.text)


    def request_campaign(self, campaign=None, lead=None):

        if not campaign or not isinstance(campaign, (str, unicode)):
            raise ValueError('Must supply campaign id as a non empty string.')

        if not lead or not isinstance(lead, (str, unicode)):
            raise ValueError('Must supply lead id as a non empty string.')

        body = request_campaign.wrap(campaign, lead)

        response = self.request(body)
        if response.status_code == 200:
            return True
        else:
            raise Exception(response.text)

    def sync_lead(self, email=None, attributes=None):

        if not email or not isinstance(email, (str, unicode)):
            raise ValueError('Must supply lead id as a non empty string.')

        if not attributes or not (isinstance(attributes, tuple) or isinstance(attributes, dict)):
            raise ValueError('Must supply attributes as a non empty tuple or dict.')

        body = sync_lead.wrap(email, attributes)

        response = self.request(body)
        if response.status_code == 200:
            return sync_lead.unwrap(response)
        else:
            raise Exception(response.text)

    def list_m_objects(self):
        body = list_m_objects.wrap()
        response = self.request(body)
        if response.status_code == 200:
            return list_m_objects.unwrap(response)
        else:
            raise Exception(response.text)