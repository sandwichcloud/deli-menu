import cherrypy

from ingredients_db.models.instance import Instance
from ingredients_db.models.region import Region
from ingredients_db.models.zones import Zone
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
            region = session.query(Region).filter(Region.id == instance.region_id).first()
            zone = session.query(Zone).filter(Zone.id == instance.zone_id).first()

            public_keys = []
            for public_key in instance.public_keys:
                public_keys.append(public_key.key)

            # Strip out user-data
            tags = instance.tags if instance.tags is not None else {}
            del tags['user-data']

        # TODO: include some sort of instance identity document similar to aws PKCS7
        # http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html

        # TODO: include some sort of service account (IAM) for the instance.
        # This will allow the instance to call the api. We probably need better acls first.

        # Those probably should be moved to a /security-creds route ^

        metadata = {
            'ami-id': instance.image_id,
            'instance-id': instance.id,
            'region': region.name,
            'availability-zone': zone.name,
            'tags': tags,
            'public-keys': public_keys
        }

        return metadata
