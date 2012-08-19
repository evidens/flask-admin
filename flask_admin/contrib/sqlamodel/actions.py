"""
Admin actions available to model-based views
"""

from werkzeug.exceptions import Forbidden
from flask import flash
from flask.ext.admin.babel import gettext as _

def primary_key_in(model, id_list):
    """
    Retrieves the primary key for given model.

    Assumes a single primary key but would work if searching by the first key
    in a multiple-key situation
    """
    primary_key = getattr(model, model.__mapper__.primary_key[0].name)
    return primary_key.in_(list(id_list))

def delete_selected(adminmodel, request, id_list):
    if not (adminmodel.is_accessible() or adminmodel.can_delete):
        raise Forbidden(_('You are not allowed to delete this.'))

    model = adminmodel.model
    model.query.filter(primary_key_in(model, id_list)).delete(
                                                synchronize_session='fetch')
    adminmodel.session.commit()
    adminmodel.session.expire_all()

    flash('You deleted the selected models.')
    return None
delete_selected.label = "Delete selected items."

all_actions = {'delete_selected': delete_selected}

