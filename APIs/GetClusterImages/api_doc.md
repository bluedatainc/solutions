**Retrieve available cluster images**
----

* **Service ID:** edp-bd-01

* **URL**
  Example: /api/v1/tenant/3

* **API Type:**  `GET`

*  **URL Params**
   Provide any params. Separate into optional and required. Document data constraints.

   **Required:**
   `tenant-id=[integer]`

* **Response/Status:**
  The expected response code!

  * **Code:** 200 <br />

* **Error Response:**
  What error response codes can be returned and what they mean.

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Invalid Login" }`

    Or

  * **Code:** 402 INVALID ID <br />
    **Content:** `{ error : "Invalid ID" }`

* **Usage:**
  An example showing how to invoke the API. Ex: curl -X GET -H "X-BDS-SESSION:/api/v1/session/session-id" http://127.0.0.1:8080/api/v1/tenant/3_

* **Additional:**
  _Additional comments, notes about the API call._
