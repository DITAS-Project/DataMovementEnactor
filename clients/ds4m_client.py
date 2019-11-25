from clients.http_common import GenericClient


class DS4Mclient(GenericClient):

    def notify_new_dal(self, dal_ip, dal_id):
        url = self.endpoint + '/NotifyDALMoved/'
        data = {
            'dalID': dal_id,
            'dalNewIP': dal_ip
        }

        response = self.put(url, data)
        return response

