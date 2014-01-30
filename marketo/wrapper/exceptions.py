from xml.etree import ElementTree as ET


class MktException(Exception):
    pass


class MktAuthenticationFailed(MktException):
    pass


class MktLeadKeyTypeNotSupported(MktException):
    pass


class MktLeadNotFound(MktException):
    pass


class MktUnknownLeadField(MktException):
    pass


class MktBadParameter(MktException):
    pass


_ERROR_MAP = {
    20014: MktAuthenticationFailed,
    # 20016: ERROR_REQUEST_TIMESTAMP_ERROR,

    20102: MktLeadKeyTypeNotSupported,
    20103: MktLeadNotFound,
    20105: MktUnknownLeadField,

    20114: MktBadParameter
}


def unwrap(exception_message):
    ret_exception = MktException("Marketo exception message parsing error: %s" % exception_message)
    try:
        root = ET.fromstring(exception_message)
        if root.find(".//detail"):
            # name = root.find(".//name").text
            message = root.find(".//message").text
            code = int(root.find(".//code").text)
            ret_exception = _ERROR_MAP.get(code, MktException)(message)
        else:
            message = root.find(".//faultstring").text
            ret_exception = MktException(message)
    except Exception as e:
        pass
    return ret_exception