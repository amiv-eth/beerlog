# API Endpoints Documentation

_This is not very important if you do not want to build your own application for reporting product consumptions._

To test the responses quickly, use [Postman](getpostman.com) and create a GET/POST request to the url of a running beerlog server, ensure to set the apikey in the header.

There are two endpoints available:

## Response Structure

All API responses are of type `application/json`.

### Success Response

All successfull requests have at least the following content:

```json
{
    "_status": "OK"
}
```

### Error Response

All error responses have the following structure:

```json
{
    "_status": "ERR",
    "_error": {
        "code": "<http-status-code>",
        "message": "error description",
    }
}
```

## GET /api/check/\<rfid\>

Check available free drinks for the given RFID number. This endpoint will only return values for the products for which the apikey has permissions.

Needs the header `Authorization: <apikey>`.

### Responses

* `HTTP 401` : Header `Authorization` is missing.
* `HTTP 403` : Provided apikey in `Authorization` header is invalid or has not enough permissions.
* `HTTP 404` : User with given RFID number does not exist.
* `HTTP 200` : Request is valid

## POST /api/report

Report a product consumption.

**Attention!**
Do report the consumption BEFORE you release the product! See responses below for more information.

Needs the header `Authorization: <apikey>`.

Needs `application/json` body with the following structure:

```json
{
    "rfid": "<rfid>",
    "product": "coffee|beer",
    "organisation": "amiv|vis|vmp"
}
```

The available values for keys `product` and `organisation` can be found in [models/enums.py](app/models/enums.py).

### Responses

* `HTTP 401` : Header `Authorization` is missing.
* `HTTP 403` : Provided apikey in `Authorization` header is invalid, has not enough permissions or the user has used up his free contingent.
* `HTTP 404` : User with given RFID number does not exist.
* `HTTP 422` : The provided request body is invalid. See key `_issues` in the error response body.
* `HTTP 201` : Consumption successfully recorded.
