from clients.http_common import GenericClient


class DEclient(GenericClient):

    def create_dal(self, blueprint_id, vdc_id, infra_id, dal_id):
        url = self.endpoint + '/blueprint/{}/vdc/{}/{}/dal?id={}'.format(blueprint_id, vdc_id, infra_id, dal_id)

        response = self.post(url, data=None)

        return response

