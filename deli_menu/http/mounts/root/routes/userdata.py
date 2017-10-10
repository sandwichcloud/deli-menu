import cherrypy
import yaml

from ingredients_db.models.instance import Instance
from ingredients_http.route import Route
from ingredients_http.router import Router


class UserDataRouter(Router):
    def __init__(self):
        super().__init__(uri_base='user-data')

    @Route()
    def get(self):
        with cherrypy.request.db_session() as session:
            instance = session.query(Instance).filter(Instance.id == cherrypy.request.instance_id).first()

            data = instance.tags.get('user-data', {
                # 'ssh_authorized_keys': [
                # ]
            })

            output = yaml.safe_dump(data=data, default_flow_style=False)
            output = "#cloud-config\n" + output
            return output
