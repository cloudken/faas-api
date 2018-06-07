
import six
from six.moves import http_client


def _cleanse_dict(original):
    """Strip all admin_password, new_pass, rescue_pass keys from a dict."""
    return dict((k, v) for k, v in original.items() if "_pass" not in k)


class CloudframeException(Exception):
    """Base Cloudframe Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = "An unknown exception occurred."
    code = http_client.INTERNAL_SERVER_ERROR
    headers = {}
    safe = False
    value = "No value."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.message % kwargs

            except Exception:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                message = self.message
                '''
                LOG.exception(_LE('Exception in string format operation'))
                for name, value in kwargs.items():
                    LOG.error("%s: %s" % (name, value))

                if CONF.fatal_exception_format_errors:
                    raise e
                else:
                    # at least get the core message out if something happened
                    message = self.message
                '''

        super(CloudframeException, self).__init__(message)

    def __str__(self):
        """Encode to utf-8 then wsme api can consume it as well."""
        if not six.PY3:
            return unicode(self.args[0]).encode('utf-8')

        return self.args[0]

    def __unicode__(self):
        """Return a unicode representation of the exception message."""
        return unicode(self.args[0])

    def format_message(self):
        if self.__class__.__name__.endswith('_Remote'):
            return self.args[0]
        else:
            return six.text_type(self)


# base class: resource can not found
class NotFound(CloudframeException):
    message = "Resource could not be found."
    code = http_client.NOT_FOUND


class Invalid(CloudframeException):
    message = "Unacceptable parameters."
    code = http_client.BAD_REQUEST


class HttpError(CloudframeException):
    message = "Http error"
    code = http_client.INTERNAL_SERVER_ERROR


class FunctionNotFound(CloudframeException):
    message = "Function for %(fun)s could not be found."
    code = http_client.METHOD_NOT_ALLOWED


class ObjectNotFound(CloudframeException):
    message = "Object for %(object)s could not be found."
    code = http_client.NOT_FOUND


class ParameterInvalid(CloudframeException):
    message = "Parameter [k: %(key)s, v: %(value)s] is invalid."
    code = http_client.BAD_REQUEST


class CreateError(CloudframeException):
    message = "Creation for %(object)s error!"
    code = http_client.INTERNAL_SERVER_ERROR


class ImageNotFound(CloudframeException):
    message = "Image for [%(res)s, %(opr)s] could not be found."
    code = http_client.NOT_FOUND
