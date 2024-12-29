from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Dict, Iterator, List

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class CloudFrontConfiguration(DictWrapper):
    @property
    def distribution_domain_name(self) -> str:
        """The domain name of the distribution that's associated with
        the request.

        """
        return self["distributionDomainName"]

    @property
    def distribution_id(self) -> str:
        """The ID of the distribution that's associated with the
        request.

        """
        # The documentation has examples of both key names, so try
        # one, then the other.
        return (
            self["distributionID"]
            if "distributionID" in self
            else self["distributionId"]
        )

    @property
    def event_type(self) -> str:
        """The type of trigger that's associated with the request:
        ``"viewer-request"``, ``"origin-request"``,
        ``"origin-response"``, or ``"viewer-response"``.

        """
        return self["eventType"]

    @property
    def request_id(self) -> str:
        """An encrypted string that uniquely identifies a
        viewer-to-CloudFront request.  The value also appears in
        CloudFront access logs as ``x-edge-request-id``.

        """
        return self["requestId"]


class CloudFrontRequestABC(DictWrapper, metaclass=ABCMeta):
    """Abstract base class from which all CloudFrontRequests inherit."""

    @property
    @abstractmethod
    def client_ip(self):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @property
    @abstractmethod
    def method(self):
        pass

    @property
    @abstractmethod
    def querystring(self):
        pass

    @property
    @abstractmethod
    def uri(self):
        pass

    @property
    @abstractmethod
    def body(self):
        pass

    @property
    @abstractmethod
    def origin(self):
        pass


class CloudFrontRequest(CloudFrontRequestABC):
    @property
    def client_ip(self) -> str:
        """The IP address of the viewer that made the request.  If the
        viewer used an HTTP proxy or a load balancer to send the
        request, the value is the IP address of the proxy or load
        balancer.

        """
        return self["clientIp"]

    @property
    def headers(self) -> Dict[str, List[Dict[str, str]]]:
        """The headers in the request.  Note the following:

        - The keys in the headers object are lowercase versions of
          standard HTTP header names.  Using lowercase keys gives you
          case-insensitive access to the header values.

        - Each header object (for example, ``headers["accept"]`` or
          ``headers["host"]``) is an array of key-value pairs.  For a
          given header, the array contains one key-value pair for each
          value in the request.

        - ``key`` contains the case-sensitive name of the header as it
          appeared in the HTTP request; for example, ``"Host"``,
          ``"User-Agent"``, ``"X-Forwarded-For"``, and so on.

        - ``value`` contains the header value as it appeared in the
          HTTP request.

        When your Lambda function adds or modifies request headers and
        you don't include the header key field, Lambda@Edge
        automatically inserts a header key using the header name that
        you provide.  Regardless of how you've formatted the header
        name, the header key that's inserted automatically is
        formatted with initial capitalization for each part, separated
        by hyphens (-).

        """
        return self["headers"]

    # TODO: @headers.setter, encapsulate?

    @property
    def method(self) -> str:
        """The HTTP method of the request."""
        return self["method"]

    @property
    def querystring(self) -> str:
        """The query string, if any, in the request.  If the request
        doesn't include a query string, the event object still
        includes querystring with an empty value."""
        return self["querystring"]

    # TODO: @querystring.setter

    @property
    def uri(self) -> str:
        """The relative path of the requested object.  If your Lambda
        function modifies the uri value, note the following:

        - The new uri value must begin with a forward slash (/).

        - When a function changes the uri value, that changes the
          object that the viewer is requesting.

        - When a function changes the uri value, that doesn't change
          the cache behavior for the request or the origin to which
          the request is sent.

        """
        return self["uri"]

    # TODO: @uri.setter

    @property
    def body(self) -> str:
        """The body of the HTTP request."""
        return self["body"]

    # TODO: @body.setter, encapsulate?


class CloudFrontViewerRequest(CloudFrontRequest):
    @property
    def origin(self):
        raise TypeError("This is not an origin request event.")


class CloudFrontOriginRequest(CloudFrontRequest):
    @property
    def origin(self):
        """The origin to which to send the request.  The origin
        structure must contain exactly one origin, which can be a
        custom origin or an Amazon S3 origin.

        """
        return self["origin"]

    # TODO: @origin.setter, encapsulate?


class CloudFrontResponseABC(DictWrapper, metaclass=ABCMeta):
    """Abstract base class from which all CloudFrontResponses inherit."""

    @property
    @abstractmethod
    def headers(self):
        pass

    @property
    @abstractmethod
    def status(self):
        pass

    @property
    @abstractmethod
    def status_description(self):
        pass


class CloudFrontResponse(CloudFrontResponseABC):
    @property
    def headers(self) -> Dict[str, List[Dict[str, str]]]:
        """The headers in the response.  Note the following:

        - The keys in the headers object are lowercase versions of
          standard HTTP header names.  Using lowercase keys gives you
          case-insensitive access to the header values.

        - Each header object (for example, ``headers["content-type"]``
          or ``headers["content-length"]``) is an array of key-value
          pairs.  For a given header, the array contains one key-value
          pair for each value in the response.

        - ``key`` contains the case-sensitive name of the header as it
          appears in the HTTP response; for example,
          ``"Content-Type"``, ``"Content-Length"``, ``"Cookie"``, and
          so on.

        - ``value`` contains the header value as it appears in the
          HTTP response.

        When your Lambda function adds or modifies response headers
        and you don't include the header key field, Lambda@Edge
        automatically inserts a header key using the header name that
        you provide.  Regardless of how you've formatted the header
        name, the header key that's inserted automatically is
        formatted with initial capitalization for each part, separated
        by hyphens (-).

        """
        return self["headers"]

    # TODO: @headers.setter, encapsulate?

    @property
    def status(self) -> str:
        """The HTTP status code of the response."""
        return self["status"]

    @property
    def status_description(self) -> str:
        """The HTTP status description of the response."""
        return self["statusDescription"]


class CloudFrontOriginResponse(CloudFrontResponse):
    pass


class CloudFrontViewerResponse(CloudFrontResponse):
    pass


class CloudFrontRecordABC(DictWrapper, metaclass=ABCMeta):
    """Abstract base class from which all CloudFrontRecords inherit."""

    @property
    @abstractmethod
    def cf_config(self):
        pass

    @property
    @abstractmethod
    def cf_request(self):
        pass

    @property
    @abstractmethod
    def cf_response(self):
        pass


class CloudFrontRecordMeta(ABCMeta):
    """Metaclass for the CloudFrontRecord class.  Sets the ``opts``
    class attribute, which holds the CloudFrontRecord class's ``class
    Meta`` options.

    """

    def __new__(mcs, name, bases, attrs):
        class_ = super().__new__(mcs, name, bases, attrs)
        meta = class_.Meta
        class_.opts = class_.OPTIONS_CLASS(meta)
        return class_


class CloudFrontRecordOptions:
    """Class meta options for :class:`CloudFrontRecord`."""

    def __init__(self, meta):
        match getattr(meta, "event", None):
            case "viewer-request":
                self.request_type = CloudFrontViewerRequest
                self.response_type = None
            case "origin-request":
                self.request_type = CloudFrontOriginRequest
                self.response_type = None
            case "origin-response":
                self.request_type = CloudFrontOriginRequest
                self.response_type = CloudFrontOriginResponse
            case "viewer-response":
                self.request_type = CloudFrontViewerRequest
                self.response_type = CloudFrontViewerResponse
            case _:
                self.request_type = None
                self.response_type = None


class CloudFrontRecord(CloudFrontRecordABC, metaclass=CloudFrontRecordMeta):
    OPTIONS_CLASS = CloudFrontRecordOptions  # type: type

    # This gets set by CloudFrontRecordMeta.
    opts = None  # type: CloudFrontRecordOptions

    class Meta:
        """Options object for a CloudFrontRecord.

        Example usage: ::

            class Meta:
                event = "viewer-request"

        Available options:

        - ``event``: Specifies the event structure; one of
          ``"viewer-request"``, ``"origin-request"``,
          ``"origin-response"``, or ``"viewer-response"``.

        """

    @property
    def cf_config(self) -> CloudFrontConfiguration:
        return CloudFrontConfiguration(self["cf"]["config"])

    @property
    def cf_request(self) -> CloudFrontRequest:
        if self.opts.request_type is None:
            raise NotImplementedError
        return self.opts.request_type(self["cf"]["request"])

    @property
    def cf_response(self) -> CloudFrontResponse:
        if self.opts.response_type is None:
            raise NotImplementedError
        return self.opts.response_type(self["cf"]["response"])


class CloudFrontViewerRequestRecord(CloudFrontRecord):
    class Meta:
        event = "viewer-request"

    @property
    def cf_request(self) -> CloudFrontViewerRequest:
        return super().cf_request


class CloudFrontOriginRequestRecord(CloudFrontRecord):
    class Meta:
        event = "origin-request"

    @property
    def cf_request(self) -> CloudFrontOriginRequest:
        return super().cf_request


class CloudFrontOriginResponseRecord(CloudFrontRecord):
    class Meta:
        event = "origin-response"

    @property
    def cf_request(self) -> CloudFrontOriginRequest:
        return super().cf_request

    @property
    def cf_response(self) -> CloudFrontOriginResponse:
        return super().cf_response


class CloudFrontViewerResponseRecord(CloudFrontRecord):
    class Meta:
        event = "viewer-response"

    @property
    def cf_request(self) -> CloudFrontViewerRequest:
        return super().cf_request

    @property
    def cf_response(self) -> CloudFrontViewerResponse:
        return super().cf_response


class CloudFrontEventABC(DictWrapper, metaclass=ABCMeta):
    """Abstract base class from which all CloudFrontEvents inherit."""

    @property
    @abstractmethod
    def record(self):
        pass

    @property
    @abstractmethod
    def records(self):
        pass


class CloudFrontEventMeta(ABCMeta):
    """Metaclass for the CloudFrontEvent class.  Sets the ``opts``
    class attribute, which holds the CloudFrontEvent class's ``class
    Meta`` options.

    """

    def __new__(mcs, name, bases, attrs):
        class_ = super().__new__(mcs, name, bases, attrs)
        meta = class_.Meta
        class_.opts = class_.OPTIONS_CLASS(meta)
        return class_


class CloudFrontEventOptions:
    """Class meta options for :class:`CloudFrontEvent`."""

    def __init__(self, meta):
        match getattr(meta, "event", None):
            case "viewer-request":
                self.record_type = CloudFrontViewerRequestRecord
            case "origin-request":
                self.record_type = CloudFrontOriginRequestRecord
            case "origin-response":
                self.record_type = CloudFrontOriginResponseRecord
            case "viewer-response":
                self.record_type = CloudFrontViewerResponseRecord
            case _:
                self.record_type = None


class CloudFrontEvent(CloudFrontEventABC, metaclass=CloudFrontEventMeta):
    OPTIONS_CLASS = CloudFrontEventOptions  # type: type

    # This gets set by CloudFrontEventMeta.
    opts = None  # type: CloudFrontEventOptions

    class Meta:
        """Options object for a CloudFrontEvent.

        Example usage: ::

            class Meta:
                event = "viwer-request"

        Available options:

        - ``event``: Specifies the event structure; one of
          ``"viewer-request"``, ``"origin-request"``,
          ``"origin-response"``, or ``"viewer-response"``.

        """

    # FIXME: The documentation implies that each event will only have
    # one record; cf. https://stackoverflow.com/a/76836588.
    @property
    def record(self) -> CloudFrontRecord:
        if self.opts.record_type is None:
            raise NotImplementedError
        return self.opts.record_type(self["Records"][0])

    @property
    def records(self) -> Iterator[CloudFrontRecord]:
        if self.opts.record_type is None:
            raise NotImplementedError
        for record in self["Records"]:
            yield self.opts.record_type(record)


class CloudFrontViewerRequestEvent(CloudFrontEvent):
    class Meta:
        event = "viewer-request"

    @property
    def record(self) -> CloudFrontViewerRequestRecord:
        return super().record

    @property
    def records(self) -> Iterator[CloudFrontViewerRequestRecord]:
        return super().records


class CloudFrontOriginRequestEvent(CloudFrontEvent):
    class Meta:
        event = "origin-request"

    @property
    def record(self) -> CloudFrontOriginRequestRecord:
        return super().record

    @property
    def records(self) -> Iterator[CloudFrontOriginRequestRecord]:
        return super().records


class CloudFrontOriginResponseEvent(CloudFrontEvent):
    class Meta:
        event = "origin-response"

    @property
    def record(self) -> CloudFrontOriginResponseRecord:
        return super().record

    @property
    def records(self) -> Iterator[CloudFrontOriginResponseRecord]:
        return super().records


class CloudFrontViewerResponseEvent(CloudFrontEvent):
    class Meta:
        event = "viewer-response"

    @property
    def record(self) -> CloudFrontViewerResponseRecord:
        return super().record

    @property
    def records(self) -> Iterator[CloudFrontViewerResponseRecord]:
        return super().records
