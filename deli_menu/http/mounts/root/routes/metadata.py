import cherrypy

from ingredients_db.models.instance import Instance
from ingredients_http.route import Route
from ingredients_http.router import Router


class MetaDataRouter(Router):
    def __init__(self):
        super().__init__(uri_base='meta-data')

    @Route()
    @cherrypy.tools.json_out()
    def get(self):
        with cherrypy.request.db_session() as session:
            instance = session.query(Instance).filter(Instance.id == cherrypy.request.instance_id).first()

        # TODO: include some sort of instance identity document similar to aws PKCS7
        # http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html

        # TODO: include some sort of service account (IAM) for the instance.
        # This will allow the instance to call the api. We probably need better acls first.

        metadata = {
            'instance-id': instance.id,
            'tags': instance.tags if instance.tags is not None else {},
            'public-keys': [
                # TODO: grab public keys from database
            ]
        }

        return metadata
