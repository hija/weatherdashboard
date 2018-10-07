import server
import waitress

waitress.serve(server.create_app(), port=8080, url_scheme='http', url_prefix='/tmp_logger')
