from __future__ import annotations

from abc import ABCMeta, abstractmethod

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class CloudFrontConfiguration(DictWrapper):
    """The CloudFront distribution's configuration and request
    information.

    """

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
        return self["distributionID"] if "distributionID" in self else self["distributionId"]

    @property
    def event_type(self) -> str:
        """The type of trigger that's associated with the request:
        `"viewer-request"`, `"origin-request"`, `"origin-response"`,
        or `"viewer-response"`.

        """
        return self["eventType"]

    @property
    def request_id(self) -> str:
        """An encrypted string that uniquely identifies a
        viewer-to-CloudFront request.  The value also appears in
        CloudFront access logs as `x-edge-request-id`.

        """
        return self["requestId"]


class CloudFrontRequestABC(DictWrapper, metaclass=ABCMeta):
    """Abstract base class for :class:`CloudFrontRequest`."""

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

    @querystring.setter
    @abstractmethod
    def querystring(self, value):
        pass

    @property
    @abstractmethod
    def uri(self):
        pass

    @uri.setter
    @abstractmethod
    def uri(self, value):
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
    """A CloudFront request object."""

    @property
    def client_ip(self) -> str:
        """The IP address of the viewer that made the request.  If the
        viewer used an HTTP proxy or a load balancer to send the
        request, the value is the IP address of the proxy or load
        balancer.

        """
        return self["clientIp"]

    @property
    def headers(self) -> dict[str, list[dict[str, str]]]:
        """The headers in the request.  Note the following:

        - The keys in the headers object are lowercase versions of
          standard HTTP header names.  Using lowercase keys gives you
          case-insensitive access to the header values.

        - Each header object (for example, `headers["accept"]` or
          `headers["host"]`) is an array of key-value pairs.  For a
          given header, the array contains one key-value pair for each
          value in the request.

        - `key` contains the case-sensitive name of the header as it
          appeared in the HTTP request; for example, `"Host"`,
          `"User-Agent"`, `"X-Forwarded-For"`, and so on.

        - `value` contains the header value as it appeared in the HTTP
          request.

        When your Lambda function adds or modifies request headers and
        you don't include the header key field, Lambda@Edge
        automatically inserts a header key using the header name that
        you provide.  Regardless of how you've formatted the header
        name, the header key that's inserted automatically is
        formatted with initial capitalization for each part, separated
        by hyphens (-).

        """
        return self["headers"]

    @property
    def method(self) -> str:
        """The HTTP method of the request."""
        return self["method"]

    @property
    def querystring(self) -> str:
        """The query string, if any, in the request.  If the request
        doesn't include a query string, the event object still
        includes querystring with an empty value.

        """
        return self["querystring"]

    @querystring.setter
    def querystring(self, value: str):
        self._data["querystring"] = value

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

    @uri.setter
    def uri(self, value: str):
        self._data["uri"] = value

    @property
    def body(self) -> str:
        """The body of the HTTP request."""
        return self["body"]


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


class CloudFrontResponseABC(DictWrapper, metaclass=ABCMeta):
    """Abstract base class for :class:`CloudFrontResponse`."""

    @property
    @abstractmethod
    def body(self):
        pass

    @body.setter
    @abstractmethod
    def body(self, value):
        pass

    @property
    @abstractmethod
    def body_encoding(self):
        pass

    @body_encoding.setter
    @abstractmethod
    def body_encoding(self, value):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @property
    @abstractmethod
    def status(self):
        pass

    @status.setter
    @abstractmethod
    def status(self, value):
        pass

    @property
    @abstractmethod
    def status_description(self):
        pass

    @status_description.setter
    @abstractmethod
    def status_description(self, value):
        pass


class CloudFrontResponse(CloudFrontResponseABC):
    @property
    def body(self) -> str | None:
        """The body, if any, that you want CloudFront to return in the
        generated response.

        """
        return self["body"] if "body" in self else None

    @body.setter
    def body(self, value: str):
        self._data["body"] = value

    @property
    def body_encoding(self) -> str | None:
        """The encoding for the value that you specified in the body.
        The only valid encodings are `"text"` and `"base64"`.  If you
        include `body` in the response object but omit the body
        encoding, CloudFront treats the body as text.

        If you specify `body_encoding` as `"base64"` but the body is
        not valid base64, CloudFront returns an error.

        """
        return self["bodyEncoding"] if "bodyEncoding" in self else None

    @body_encoding.setter
    def body_encoding(self, value: str):
        if value not in ["text", "base64"]:
            raise ValueError(f"got {value!r}, must be either 'text' or 'base64'")
        self._data["bodyEncoding"] = value

    @property
    def headers(self) -> dict[str, list[dict[str, str]]]:
        """The headers in the response.  Note the following:

        - The keys in the headers object are lowercase versions of
          standard HTTP header names.  Using lowercase keys gives you
          case-insensitive access to the header values.

        - Each header object (for example, `headers["content-type"]`
          or `headers["content-length"]`) is an array of key-value
          pairs.  For a given header, the array contains one key-value
          pair for each value in the response.

        - `key` contains the case-sensitive name of the header as it
          appears in the HTTP response; for example, `"Content-Type"`,
          `"Content-Length"`, `"Cookie"`, and so on.

        - `value` contains the header value as it appears in the HTTP
          response.

        When your Lambda function adds or modifies response headers
        and you don't include the header key field, Lambda@Edge
        automatically inserts a header key using the header name that
        you provide.  Regardless of how you've formatted the header
        name, the header key that's inserted automatically is
        formatted with initial capitalization for each part, separated
        by hyphens (-).

        """
        return self["headers"]

    @property
    def status(self) -> str:
        """The HTTP status code of the response.

        Provide the status code as a string.  CloudFront uses the
        provided status code for the following:

        - return in the response,

        - cache in the CloudFront edge cache, when the response was
          generated by a function that was triggered by an origin
          request event, and

        - logs in CloudFront Standard logging (access logs).

        If the status value isn't between 200 and 599, CloudFront
        returns an error to the viewer.

        """
        return self["status"]

    @status.setter
    def status(self, value: str):
        self._data["status"] = value

    @property
    def status_description(self) -> str:
        """The HTTP status description of the response.

        Provide the description accompanying the HTTP status code that
        you want CloudFront to return in the response.  You don't need
        to use standard descriptions such as `"OK"` for an HTTP status
        code of 200.

        """
        return self["statusDescription"]

    @status_description.setter
    def status_description(self, value: str):
        self._data["statusDescription"] = value


class CloudFrontOriginResponse(CloudFrontResponse):
    pass


class CloudFrontViewerResponse(CloudFrontResponse):
    pass


class CloudFrontRecordABC(DictWrapper, metaclass=ABCMeta):
    """Abstract base class for :class:`CloudFrontRecord`."""

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
    """Metaclass for :class:`CloudFrontRecord`.  Sets the `opts` class
    attribute, which holds the class's configuration options.

    """

    def __new__(mcs, name, bases, attrs):
        class_ = super().__new__(mcs, name, bases, attrs)
        meta = class_.Meta
        class_.opts = class_.OPTIONS_CLASS(meta)
        return class_


class CloudFrontRecordOptions:
    """Configuration options for :class:`CloudFrontRecord`.

    This sets the following attributes depending on the `event` class
    meta configuration option:

    - `request_type`: A :class:`CloudFrontRequest` subclass, e.g., for
      a viewer-response event, :class:`CloudFrontViewerRequest`.

    - `response_type`: A :class:`CloudFrontResponse` subclass, e.g.,
      for a viewer-response event, :class:`CloudFrontViewerResponse`.

    """

    def __init__(self, meta):
        # NB: match/case is only available in Python 3.10+
        event = getattr(meta, "event", None)
        if event == "viewer-request":
            self.request_type = CloudFrontViewerRequest
            self.response_type = None
        elif event == "origin-request":
            self.request_type = CloudFrontOriginRequest
            self.response_type = None
        elif event == "origin-response":
            self.request_type = CloudFrontOriginRequest
            self.response_type = CloudFrontOriginResponse
        elif event == "viewer-response":
            self.request_type = CloudFrontViewerRequest
            self.response_type = CloudFrontViewerResponse
        else:
            self.request_type = None
            self.response_type = None


class CloudFrontRecord(CloudFrontRecordABC, metaclass=CloudFrontRecordMeta):
    """CloudFront request/response event data.

    Subclasses differ only in their configuration.  Refer to the
    options object for details.

    """

    OPTIONS_CLASS = CloudFrontRecordOptions  # type: type

    # This gets set by CloudFrontRecordMeta.
    opts = None  # type: CloudFrontRecordOptions

    class Meta:
        """Configuration options for :class:`CloudFrontRecord`.

        Example usage: ::

            class Meta:
                event = "viewer-request"

        Available options:

        - `event`: Specifies the event structure; one of
          `"viewer-request"`, `"origin-request"`, `"origin-response"`,
          or `"viewer-response"`.

        """

    @property
    def cf_config(self) -> CloudFrontConfiguration:
        return CloudFrontConfiguration(
            data=self["cf"]["config"],
            # Propagate json_deserializer to lower-level objects.
            json_deserializer=self._json_deserializer,
        )

    @property
    def cf_request(self) -> CloudFrontRequest:
        if self.opts.request_type is None:
            raise NotImplementedError
        return self.opts.request_type(
            data=self["cf"]["request"],
            # Propagate json_deserializer to lower-level objects.
            json_deserializer=self._json_deserializer,
        )

    @property
    def cf_response(self) -> CloudFrontResponse:
        if self.opts.response_type is None:
            raise NotImplementedError
        return self.opts.response_type(
            data=self["cf"]["response"],
            # Propagate json_deserializer to lower-level objects.
            json_deserializer=self._json_deserializer,
        )


class CloudFrontViewerRequestRecord(CloudFrontRecord):
    class Meta:
        event = "viewer-request"


class CloudFrontOriginRequestRecord(CloudFrontRecord):
    class Meta:
        event = "origin-request"


class CloudFrontOriginResponseRecord(CloudFrontRecord):
    class Meta:
        event = "origin-response"


class CloudFrontViewerResponseRecord(CloudFrontRecord):
    class Meta:
        event = "viewer-response"


class CloudFrontEventABC(DictWrapper, metaclass=ABCMeta):
    """Abstract base class for :class:`CloudFrontEvent`."""

    @property
    @abstractmethod
    def record(self):
        pass


class CloudFrontEventMeta(ABCMeta):
    """Metaclass for :class:`CloudFrontEvent`.  Sets the `opts` class
    attribute, which holds the class's configuration options.

    """

    def __new__(mcs, name, bases, attrs):
        class_ = super().__new__(mcs, name, bases, attrs)
        meta = class_.Meta
        class_.opts = class_.OPTIONS_CLASS(meta)
        return class_


class CloudFrontEventOptions:
    """Configuration options for :class:`CloudFrontEvent`.

    This sets the following attributes depending on the `event` class
    meta configuration option:

    - `record_type`: A :class:`CloudFrontRecord` subclass, e.g., for a
      origin-response event, :class:`CloudFrontOriginResponseRecord`.

    """

    def __init__(self, meta):
        # NB: match/case is only available in Python 3.10+
        event = getattr(meta, "event", None)
        if event == "viewer-request":
            self.record_type = CloudFrontViewerRequestRecord
        elif event == "origin-request":
            self.record_type = CloudFrontOriginRequestRecord
        elif event == "origin-response":
            self.record_type = CloudFrontOriginResponseRecord
        elif event == "viewer-response":
            self.record_type = CloudFrontViewerResponseRecord
        else:
            self.record_type = None


class CloudFrontEvent(CloudFrontEventABC, metaclass=CloudFrontEventMeta):
    """A request or response event object that CloudFront passes to a
    Lambda@Edge function when it's triggered.

    Subclasses differ only in their configuration.  Refer to the
    options object for details.

    """

    OPTIONS_CLASS = CloudFrontEventOptions  # type: type

    # This gets set by CloudFrontEventMeta.
    opts = None  # type: CloudFrontEventOptions

    class Meta:
        """Configuration options for :class:`CloudFrontEvent`.

        Example usage: ::

            class Meta:
                event = "viewer-request"

        Available options:

        - `event`: Specifies the event structure; one of
          `"viewer-request"`, `"origin-request"`, `"origin-response"`,
          or `"viewer-response"`.

        """

    # The documentation implies that each event will have one and only
    # one record; cf. https://stackoverflow.com/a/76836588.
    @property
    def record(self) -> CloudFrontRecord:
        if self.opts.record_type is None:
            raise NotImplementedError
        return self.opts.record_type(
            data=self["Records"][0],
            # Propagate json_deserializer to lower-level objects.
            json_deserializer=self._json_deserializer,
        )


class CloudFrontViewerRequestEvent(CloudFrontEvent):
    class Meta:
        event = "viewer-request"


class CloudFrontOriginRequestEvent(CloudFrontEvent):
    class Meta:
        event = "origin-request"


class CloudFrontOriginResponseEvent(CloudFrontEvent):
    class Meta:
        event = "origin-response"


class CloudFrontViewerResponseEvent(CloudFrontEvent):
    class Meta:
        event = "viewer-response"
