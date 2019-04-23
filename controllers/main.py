import logging
import operator

from odoo.tools.translate import _
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ReactSession(http.Controller):

    @http.route(['/react/session/authenticate', '/react'], type='json', auth='public', methods=['POST', 'OPTIONS'], website=False, cors='*', csrf=False)
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @http.route('/react/session/change_password', type='json', auth="user")
    def change_password(self, fields):
        old_password, new_password, confirm_password = operator.itemgetter('old_pwd', 'new_password', 'confirm_pwd')(
            dict(map(operator.itemgetter('name', 'value'), fields)))
        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            return {'error': _('You cannot leave any password empty.'), 'title': _('Change Password')}
        if new_password != confirm_password:
            return {'error': _('The new password and its confirmation must be identical.'), 'title': _('Change Password')}
        try:
            if request.env['res.users'].change_password(old_password, new_password):
                return {'new_password': new_password}
        except Exception:
            return {'error': _('The old password you provided is incorrect, your password was not changed.'), 'title': _('Change Password')}
        return {'error': _('Error, password not changed !'), 'title': _('Change Password')}
