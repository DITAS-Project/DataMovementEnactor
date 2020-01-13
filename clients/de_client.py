from clients.http_common import GenericClient
import logging


LOG = logging.getLogger()


class DEclient(GenericClient):

    def create_dal(self, blueprint_id, vdc_id, infra_id, dal_id):
        url = self.endpoint + '/blueprint/{}/vdc/{}/{}/dal?id={}'.format(blueprint_id, vdc_id, infra_id, dal_id)

        response = self.post(url, data=None)

        LOG.debug('Created DAL. Response: {}'.format(response))

        return response

    def create_datasource(self, blueprint_id, vdc_id, infra_id, type):
        url = self.endpoint + '/blueprint/{}/vdc/{}/{}/datasource?type={}&size=2Gi&id=bloodTest'.format(blueprint_id,
                                                                                                        vdc_id,
                                                                                                        infra_id,
                                                                                                        type)
        response = self.post(url, data=None)
        LOG.debug('Created datasource. Response: {}'.format(response))

        return response

    def move_dal(self, blueprint_id, vdc_id, infra_id, dal_id, dal_ip):
        url = self.endpoint + '/blueprint/{}/vdc/{}/{}/dal/{}?ip={}'.format(blueprint_id, vdc_id, infra_id, dal_id,
                                                                            dal_ip)
        response = self.put(url, data=None)
        LOG.debug('Moved DAL. Response: {}'.format(response))
        return response
