import json

import pytest

from app.traffic_parser import parse_traffic, deduplicate_traffic
from app.models import APIEndpoint


def test_parse_traffic():
    traffic = parse_traffic("data/observed_traffic.json")

    assert len(traffic) == 7

    assert traffic[0].path == "/users"
    assert traffic[0].method == "GET"
    assert traffic[0].status_code == 200
    assert traffic[0].source == "traffic"

    assert traffic[1].path == "/users"
    assert traffic[1].method == "POST"
    assert traffic[1].status_code == 201

    assert traffic[3].path == "/users/101"
    assert traffic[3].method == "DELETE"
    assert traffic[3].status_code == 204

    assert traffic[4].path == "/admin/users"
    assert traffic[4].method == "POST"
    assert traffic[4].status_code == 403
    assert traffic[4].source == "traffic"

    assert traffic[5].path == "/internal/debug"
    assert traffic[5].method == "GET"
    assert traffic[5].status_code == 200
    assert traffic[5].source == "traffic"


def test_parse_traffic_missing_method(tmp_path):
    traffic_file = tmp_path / "traffic.json"

    traffic_file.write_text(
        json.dumps([
            {"path": "/users"}
        ]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing 'method'"):
        parse_traffic(str(traffic_file))


def test_parse_traffic_missing_path(tmp_path):
    traffic_file = tmp_path / "traffic.json"

    traffic_file.write_text(
        json.dumps([
            {"method": "GET"}
        ]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing 'path'"):
        parse_traffic(str(traffic_file))


def test_deduplicate_traffic():
    observed = [
        APIEndpoint(
            path="/users/101",
            method="GET",
            source="traffic",
            status_code=200,
        ),
        APIEndpoint(
            path="/users/102",
            method="GET",
            source="traffic",
            status_code=200,
        ),
        APIEndpoint(
            path="/users/101",
            method="GET",
            source="traffic",
            status_code=200,
        ),
        APIEndpoint(
            path="/users/101",
            method="POST",
            source="traffic",
            status_code=201,
        ),
    ]

    unique = deduplicate_traffic(observed)

    assert len(unique) == 2

    assert unique[0].path == "/users/{id}"
    assert unique[0].method == "GET"
    assert unique[0].status_code == 200

    assert unique[1].path == "/users/{id}"
    assert unique[1].method == "POST"
    assert unique[1].status_code == 201
