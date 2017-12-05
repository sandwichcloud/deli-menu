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

            keypairs = []
            for keypair in instance.keypairs:
                keypairs.append(keypair.public_key)

            # Strip out user-data
            tags = instance.tags if instance.tags is not None else {}
            if 'user-data' in tags:
                del tags['user-data']

        metadata = {
            'ami-id': instance.image_id,
            'instance-id': instance.id,
            'region': region.name,
            'availability-zone': zone.name,
            'tags': tags,
            'public-keys': keypairs
        }

        return metadata
