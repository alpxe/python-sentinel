from com.base.singleton import Singleton
import requests
import json


class Pusher(Singleton):
    # 获取token API
    __TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

    # 发送消息 API
    __SEND_URL = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"

    # 获取接收者的open_id API
    __INFO_URL = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id"

    __app_id = "" # <APP_ID>
    __app_secret = "" #<APP_SECRET>

    phone = ""

    def __get_token(self):
        payload = {"app_id": self.__app_id, "app_secret": self.__app_secret}
        response = requests.post(self.__TOKEN_URL, json=payload)
        return response.json().get("tenant_access_token")

    def __get_info(self, token):
        """
        通过手机号获取员工的 open_id
        """

        params = {"user_id_type": "open_id"}
        payload = {"mobiles": [self.phone]}  # 手机号列表，单个也放列表里
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.__INFO_URL, params=params, json=payload, headers=headers)
        result = response.json()

        if result.get("code") == 0:
            user_list = result.get("data", {}).get("user_list", [])
            if user_list:
                return user_list[0].get("user_id")  # user_id就是open_id
            else:
                return None  # 未找到该手机号的用户
        else:
            raise Exception(f"查询open_id失败: {result.get('msg')}")

    def __message(self, token, usr, msg):
        payload = {
            "receive_id": usr,
            "msg_type": "text",
            "content": json.dumps({"text": msg})
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.__SEND_URL, json=payload, headers=headers)
        return response.json()

    def send_msg(self, msg):
        if self.phone and len(self.phone) > 0:
            token = self.__get_token()
            if token and len(token) > 0:
                info = self.__get_info(token)
                if info and len(info) > 0:
                    resp = self.__message(token, info, msg)
                    if resp.get("code") == 0:
                        return True
        return False
