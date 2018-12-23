from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer

from eNMS.automation.helpers import netmiko_connection
from eNMS.automation.models import Service
from eNMS.base.classes import service_classes


class ConfigurationBackupService(Service):

    __tablename__ = 'ConfigurationBackupService'

    id = Column(Integer, ForeignKey('Service.id'), primary_key=True)
    has_targets = True
    number_of_configuration = Column(Integer, default=10)

    __mapper_args__ = {
        'polymorphic_identity': 'ConfigurationBackupService',
    }

    def job(self, device, _):
        netmiko_handler = netmiko_connection(self, device)
        config = netmiko_handler.send_command(device.configuration_command)
        device.configurations[datetime.now()] = config
        if len(device.configurations > self.number_of_configuration):
            device.configurations.pop(min(device.configurations))
        return {
            'success': True,
            'result': f'Command: {device.configuration_command}'
        }


service_classes['ConfigurationBackupService'] = ConfigurationBackupService
