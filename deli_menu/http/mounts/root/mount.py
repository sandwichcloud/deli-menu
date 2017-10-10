import cherrypy

from ingredients_db.models.instance import Instance
from ingredients_db.models.network_port import NetworkPort
from ingredients_http.app import HTTPApplication
from ingredients_http.app_mount import ApplicationMount


class RootMount(ApplicationMount):
    def __init__(self, app: HTTPApplication):
        super().__init__(app=app, mount_point='/')

    def check_instance(self):
        ip_address = cherrypy.request.remote.ip

        with cherrypy.request.db_session() as session:
            instance = session.query(Instance).join(NetworkPort, Instance.network_port_id == NetworkPort.id).filter(
                NetworkPort.ip_address == ip_address).first()

            if instance is None:
                raise cherrypy.HTTPError(403, "Could not find an instance with the requested remote IP.")

            cherrypy.request.instance_id = instance.id

    def __setup_tools(self):
        cherrypy.tools.instance = cherrypy.Tool('on_start_resource', self.check_instance)

    def setup(self):
        self.__setup_tools()
        super().setup()

    def mount_config(self):
        config = super().mount_config()
        config['tools.instance.on'] = True
        return config
