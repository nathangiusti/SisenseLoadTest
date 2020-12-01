import time

from locust import HttpUser, task, events
from PySense import PySense, SisenseRole

from PySenseLoadTest import LoadTestConnector
from PySenseLoadTest import LoadTestUtils

"""START CONFIG"""
host = 'http://localhost:8081/'  # The address of the server to LoadTest
version = 'Windows'  # Whether it is a windows or Linux server
user_name_key = 'loadtest'  # Any users with this in their username will be used as test users.
password = 'MyPassword'  # The password for the test users. Script assumed all test users have the same password.
dashboard_wait_time = 10  # Time in seconds between dashboard loads
admin_config = '//Users//Documents//Config.yaml'

# An array of jaql calls to test
dashboard_base_jaql = [
    {"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0"},"metadata":[{"jaql":{"table":"Commerce","column":"Revenue","dim":"[Commerce.Revenue]","datatype":"numeric","agg":"sum","title":"Total Revenue"},"format":{"mask":{"type":"number","abbreviations":{"t":True,"b":True,"m":True,"k":False},"separated":True,"decimals":"auto","isdefault":True},"color":{"color":"#00cee6","type":"color"}},"source":"value"}],"m2mThresholdFlag":0,"isMaskedResult":True,"format":"json","widget":"5fb58bf40ab5f21530fcf6ea;","dashboard":"5fb58be90ab5f21530fcf6e7;LoadTest","queryGuid":"79A38-1F4A-8811-AE18-8132-C70B-C8E3-75A7-C","offset":0,"count":50000},
    {"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0"},"format":"pivot","count":25,"offset":0,"grandTotals":{"rows":False,"title":"Grand Total"},"metadata":[{"jaql":{"table":"Commerce","column":"Date","dim":"[Commerce.Date (Calendar)]","datatype":"datetime","merged":True,"level":"years","title":"Years in Date"},"format":{"mask":{"years":"yyyy","quarters":"yyyy Q","months":"MM/yyyy","weeks":"ww yyyy","days":"shortDate","minutes":"HH:mm","isdefault":True},"subtotal":True},"hierarchies":["calendar","calendar - weeks"],"field":{"id":"[Commerce.Date (Calendar)]_years","index":0},"panel":"rows"},{"jaql":{"table":"Brand","column":"Brand","dim":"[Brand.Brand]","datatype":"text","merged":True,"title":"Brand"},"field":{"id":"[Brand.Brand]","index":1},"panel":"rows"},{"jaql":{"table":"Commerce","column":"Revenue","dim":"[Commerce.Revenue]","datatype":"numeric","agg":"sum","title":"Total Revenue"},"format":{"mask":{"type":"number","t":True,"b":True,"separated":True,"decimals":"auto","isdefault":True},"color":{"type":"color","color":"transparent"}},"field":{"id":"[Commerce.Revenue]_sum","index":2},"panel":"measures"},{"jaql":{"table":"Commerce","column":"Quantity","dim":"[Commerce.Quantity]","datatype":"numeric","agg":"sum","title":"Total Quantity"},"format":{"mask":{"type":"number","t":True,"b":True,"separated":True,"decimals":"auto","isdefault":True},"color":{"type":"color","color":"transparent"}},"field":{"id":"[Commerce.Quantity]_sum","index":3},"panel":"measures"},{"jaql":{"table":"Commerce","column":"Revenue","dim":"[Commerce.Revenue]","datatype":"numeric","agg":"sum","title":"Total Revenue","filter":{"top":10},"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0"},"collapsed":False},"format":{"mask":{"type":"number","t":True,"b":True,"separated":True,"decimals":"auto","isdefault":True}},"panel":"scope"}],"m2mThresholdFlag":0,"isMaskedResult":True,"widget":"5fb69d5c0ab5f21530fcf772;","dashboard":"5fb58be90ab5f21530fcf6e7;LoadTest","queryGuid":"43C47-ED60-DBCD-6DBA-E6CF-5158-9048-D61A-C"}
]

dashboard_filtered_jaql = [
    {"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0","lastBuildTime":"2020-09-23T19:13:50.913Z"},"metadata":[{"dim":"[Commerce.Date (Calendar)]","sort":"desc","level":"years"}],"offset":0,"count":50,"isMaskedResponse":False,"queryGuid":"225D8-890C-52A3-C66B-D68C-1768-F780-B84D-4"},
    {"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0"},"metadata":[{"jaql":{"table":"Commerce","column":"Revenue","dim":"[Commerce.Revenue]","datatype":"numeric","agg":"sum","title":"Total Revenue"},"format":{"mask":{"type":"number","abbreviations":{"t":True,"b":True,"m":True,"k":False},"separated":True,"decimals":"auto","isdefault":True},"color":{"color":"#00cee6","type":"color"}},"source":"value"},{"jaql":{"table":"Commerce","column":"Date","dim":"[Commerce.Date (Calendar)]","datatype":"datetime","merged":True,"title":"Years in Date","level":"years","collapsed":False,"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0","lastBuildTime":"2020-09-23T19:13:50.913Z"},"filter":{"explicit":True,"multiSelection":True,"members":["2013-01-01T00:00:00","2012-01-01T00:00:00","2011-01-01T00:00:00","2010-01-01T00:00:00"]}},"isCascading":False,"panel":"scope"}],"m2mThresholdFlag":0,"isMaskedResult":True,"format":"json","widget":"5fb58bf40ab5f21530fcf6ea;","dashboard":"5fb58be90ab5f21530fcf6e7;LoadTest","queryGuid":"F3107-5121-BFAF-424B-357E-C869-CAA4-890D-D","offset":0,"count":50000},
    {"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0"},"format":"pivot","count":25,"offset":0,"grandTotals":{"rows":False,"title":"Grand Total"},"metadata":[{"jaql":{"table":"Commerce","column":"Date","dim":"[Commerce.Date (Calendar)]","datatype":"datetime","merged":True,"level":"years","title":"Years in Date"},"format":{"mask":{"years":"yyyy","quarters":"yyyy Q","months":"MM/yyyy","weeks":"ww yyyy","days":"shortDate","minutes":"HH:mm","isdefault":True},"subtotal":True},"hierarchies":["calendar","calendar - weeks"],"field":{"id":"[Commerce.Date (Calendar)]_years","index":0},"panel":"rows"},{"jaql":{"table":"Brand","column":"Brand","dim":"[Brand.Brand]","datatype":"text","merged":True,"title":"Brand"},"field":{"id":"[Brand.Brand]","index":1},"panel":"rows"},{"jaql":{"table":"Commerce","column":"Revenue","dim":"[Commerce.Revenue]","datatype":"numeric","agg":"sum","title":"Total Revenue"},"format":{"mask":{"type":"number","t":True,"b":True,"separated":True,"decimals":"auto","isdefault":True},"color":{"type":"color","color":"transparent"}},"field":{"id":"[Commerce.Revenue]_sum","index":2},"panel":"measures"},{"jaql":{"table":"Commerce","column":"Quantity","dim":"[Commerce.Quantity]","datatype":"numeric","agg":"sum","title":"Total Quantity"},"format":{"mask":{"type":"number","t":True,"b":True,"separated":True,"decimals":"auto","isdefault":True},"color":{"type":"color","color":"transparent"}},"field":{"id":"[Commerce.Quantity]_sum","index":3},"panel":"measures"},{"jaql":{"table":"Commerce","column":"Revenue","dim":"[Commerce.Revenue]","datatype":"numeric","agg":"sum","title":"Total Revenue","filter":{"top":10},"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0"},"collapsed":False},"format":{"mask":{"type":"number","t":True,"b":True,"separated":True,"decimals":"auto","isdefault":True}},"panel":"scope"},{"jaql":{"table":"Commerce","column":"Date","dim":"[Commerce.Date (Calendar)]","datatype":"datetime","merged":True,"title":"Years in Date","level":"years","collapsed":False,"datasource":{"title":"Sample ECommerce","fullname":"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost","database":"aSampleIAAaECommerce","oid":"3d84caac-e089-47c6-8583-f12abe7318b0","lastBuildTime":"2020-09-23T19:13:50.913Z"},"filter":{"explicit":True,"multiSelection":True,"members":["2013-01-01T00:00:00","2012-01-01T00:00:00","2011-01-01T00:00:00","2010-01-01T00:00:00"]}},"isCascading":False,"panel":"scope"}],"m2mThresholdFlag":0,"isMaskedResult":True,"widget":"5fb69d5c0ab5f21530fcf772;","dashboard":"5fb58be90ab5f21530fcf6e7;LoadTest","queryGuid":"A87BE-9921-467F-7C7B-4C8D-8E1B-730C-F4D4-7"}
]

dashboards = [dashboard_base_jaql, dashboard_filtered_jaql]
"""END CONFIG"""

counter = 0
token_array = []


def get_token():
    global counter
    counter += 1
    if counter >= len(token_array):
        counter = 0
    return token_array[counter]


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    global token_array
    py_client = PySense.authenticate_by_file(admin_config)
    all_viewers = py_client.get_users(role=SisenseRole.Role.VIEWER)
    test_users = []
    for user in all_viewers:
        if user_name_key in user.get_email():
            test_users.append(user)
    token_array = LoadTestUtils.generate_tokens(host, test_users, password)


class LoadTestUser(HttpUser):

    @task
    def test_task(self):
        py_client = PySense.authenticate_custom_connector(
            version, LoadTestConnector.LoadTestConnector(host, get_token(), self.client))
        for dashboard in dashboards:
            for query in dashboard:
                py_client.connector.rest_call('post', 'api/datasources/Sample%20ECommerce/jaql', json_payload=query)
            time.sleep(dashboard_wait_time)

