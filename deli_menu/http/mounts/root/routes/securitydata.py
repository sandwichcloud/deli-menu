import json

import arrow
import cherrypy
from cryptography.fernet import Fernet
from simple_settings import settings

from ingredients_db.models.authn import AuthNServiceAccount
from ingredients_db.models.instance import Instance
from ingredients_http.route import Route
from ingredients_http.router import Router


class SecurityDataRouter(Router):
    def __init__(self):
        super().__init__(uri_base='security-data')

    @Route()
    @cherrypy.tools.json_out()
    def get(self):
        with cherrypy.request.db_session() as session:
            instance = session.query(Instance).filter(Instance.id == cherrypy.request.instance_id).first()
            service_account: AuthNServiceAccount = session.query(AuthNServiceAccount).filter(
                AuthNServiceAccount.id == instance.service_account_id).first()

        fernet = Fernet(settings.AUTH_FERNET_KEYS[0])

        token_data = {
            # Token only lasts 30 minutes. This should be more than enough
            'expires_at': arrow.now().shift(minute=+30),
            'service_account_id': service_account.id,
            'project_id': instance.project_id,
            'roles': {
                'global': [],
                'project': [service_account.role_id]
            }
        }

        # TODO: these will be generated every time an instance asks for it
        # Should be cached these somewhere?
        return {
            "token": fernet.encrypt(json.dumps(token_data).encode()).decode()
        }
