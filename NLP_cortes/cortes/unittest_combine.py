# 4 space 
import unittest
import requests
import json

class RequestsTestCase(unittest.TestCase):

    def test_get_infocontent(self):
        info_obj = info_test()
        expected = {  "async_call": False,  "fapp_name": "fappParker",  "host_ip": "100.64.119.33",  "host_name": "parker2",  "lucene": False}
        self.assertEqual(info_obj.get_infocontent(), expected)

    def test_get_echocontent(self):
        echo_obj = echo_test()
        expected = {"key1":["value1"],"key2":["value2"]}
        self.assertEqual(echo_obj.get_echocontent(), expected)

    def test_post_echocontent(self):
        echo_obj = echo_test()
        expected = {"key1": "value1","key2": "value2","status": "ok"}
        self.assertEqual(echo_obj.post_echocontent(), expected)


class info_test:
    def get_infocontent(self):
        r = requests.get("http://100.64.119.33:35000/info")
        res = r.content
        dic = json.loads(res)#change to dic
        return dic


class echo_test:
    def get_echocontent(self):
        payload = {'key1':'value1', 'key2':'value2'}
        r = requests.get("http://100.64.119.33:35000/echo", params=payload)
        r_temp = r.content
        dic = json.loads(r_temp)
        return dic

    def post_echocontent(self):
        payload = {'key1':'value1', 'key2':'value2'}
        headers = {'content-type': 'application/json'}
        r = requests.post("http://100.64.119.33:35000/echo", data=json.dumps(payload), headers=headers)
        r_temp = r.content
        dic = json.loads(r_temp)
        return dic


if __name__ == '__main__':
    unittest.main()
