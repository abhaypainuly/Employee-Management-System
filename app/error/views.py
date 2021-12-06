from flask import render_template, abort

from . import error

@error.app_errorhandler(403)
def forbidden(error):
    return render_template("error/403.html", title="Forbidden"), 403

@error.app_errorhandler(404)
def page_not_found(error):
    return render_template("error/404.html", title="Page Not Found"), 404

@error.app_errorhandler(500)
def internal_server_error(error):
    return render_template("error/500.html", title="Internal Service Error"), 500