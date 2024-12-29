import json

import pytest

from aws_lambda_powertools.utilities.data_classes.cloudfront_event import (
    CloudFrontConfiguration,
    CloudFrontOriginRequest,
    CloudFrontOriginRequestEvent,
    CloudFrontOriginRequestRecord,
    CloudFrontOriginResponse,
    CloudFrontOriginResponseEvent,
    CloudFrontOriginResponseRecord,
    CloudFrontViewerRequest,
    CloudFrontViewerRequestEvent,
    CloudFrontViewerRequestRecord,
    CloudFrontViewerResponse,
    CloudFrontViewerResponseEvent,
    CloudFrontViewerResponseRecord,
)
from tests.functional.utils import load_event


def test_cloudfront_viewer_request_event():
    raw_event = load_event("cloudFrontViewerRequestEvent.json")
    parsed_event = CloudFrontViewerRequestEvent(raw_event)
    records = list(parsed_event.records)

    assert len(records) == 1
    assert isinstance(records[0], CloudFrontViewerRequestRecord)
    assert parsed_event.record
    assert isinstance(parsed_event.record, CloudFrontViewerRequestRecord)
    assert parsed_event.record.cf_config
    assert isinstance(parsed_event.record.cf_config, CloudFrontConfiguration)
    assert (
        parsed_event.record.cf_config.distribution_domain_name
        == "d111111abcdef8.cloudfront.net"
    )
    assert parsed_event.record.cf_config.distribution_id == "EDFDVBD6EXAMPLE"
    assert parsed_event.record.cf_config.event_type == "viewer-request"
    assert (
        parsed_event.record.cf_config.request_id
        == "4TyzHTaYWb1GX1qTfsHhEqV6HUDd_BzoBZnwfnvQc_1oF26ClkoUSEQ=="
    )
    assert parsed_event.record.cf_request
    assert isinstance(parsed_event.record.cf_request, CloudFrontViewerRequest)
    assert parsed_event.record.cf_request.client_ip == "203.0.113.178"
    assert "host" in parsed_event.record.cf_request.headers
    assert parsed_event.record.cf_request.method == "GET"
    assert parsed_event.record.cf_request.querystring == ""
    assert parsed_event.record.cf_request.uri == "/"
    with pytest.raises(KeyError):
        parsed_event.record.cf_request.body
    with pytest.raises(TypeError):
        parsed_event.record.cf_request.origin
    with pytest.raises(NotImplementedError):
        parsed_event.record.cf_response


def test_cloudfront_origin_request_event():
    raw_event = load_event("cloudFrontOriginRequestEvent.json")
    parsed_event = CloudFrontOriginRequestEvent(raw_event)
    records = list(parsed_event.records)

    assert len(records) == 1
    assert isinstance(records[0], CloudFrontOriginRequestRecord)
    assert parsed_event.record
    assert isinstance(parsed_event.record, CloudFrontOriginRequestRecord)
    assert parsed_event.record.cf_config.event_type == "origin-request"
    assert parsed_event.record.cf_request
    assert isinstance(parsed_event.record.cf_request, CloudFrontOriginRequest)
    assert parsed_event.record.cf_request.origin
    assert "custom" in parsed_event.record.cf_request.origin
    assert "domainName" in parsed_event.record.cf_request.origin["custom"]
    assert parsed_event.record.cf_request.origin["custom"]["keepaliveTimeout"] == 5


def test_cloudfront_origin_response_event():
    raw_event = load_event("cloudFrontOriginResponseEvent.json")
    parsed_event = CloudFrontOriginResponseEvent(raw_event)
    records = list(parsed_event.records)

    assert len(records) == 1
    assert isinstance(records[0], CloudFrontOriginResponseRecord)
    assert parsed_event.record
    assert parsed_event.record.cf_request
    assert isinstance(parsed_event.record, CloudFrontOriginResponseRecord)
    assert parsed_event.record.cf_response
    assert isinstance(parsed_event.record.cf_response, CloudFrontOriginResponse)
    assert "access-control-allow-credentials" in parsed_event.record.cf_response.headers
    assert parsed_event.record.cf_response.status == "200"
    assert parsed_event.record.cf_response.status_description == "OK"


def test_cloudfront_viewer_response_event():
    raw_event = load_event("cloudFrontViewerResponseEvent.json")
    parsed_event = CloudFrontViewerResponseEvent(raw_event)
    records = list(parsed_event.records)

    assert len(records) == 1
    assert isinstance(records[0], CloudFrontViewerResponseRecord)
    assert parsed_event.record
    assert parsed_event.record.cf_request
    assert isinstance(parsed_event.record, CloudFrontViewerResponseRecord)
    assert parsed_event.record.cf_response
    assert isinstance(parsed_event.record.cf_response, CloudFrontViewerResponse)
    assert parsed_event.record.cf_response
