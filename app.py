from flask import Flask, request, redirect
from flask_restx import Api, Resource

from database import Link, Base, engine

app = Flask(__name__)
api = Api(app)

@app.before_request
def func():
    Base.metadata.create_all(bind=engine)

@app.route('/<code>')
def redirect_links(code):
    link = Link.get_link_by_code(code)
    if link:
        return redirect(link.original_link)
    else:
        return {'error': 'link not found'}, 404

@api.route('/api/links')
class Links(Resource):
    def post(self):
        data = request.json
        print(data)
        origin_link = data.get('origin_link')
        link = Link.link_generation(origin_link)
        host = request.host
        return {'short_link': f'{host}/{link.short_code}', 'id': link.id}

    def get(self):
        data = request.json
        code = data.get('code')
        if code:
            link = Link.get_link_by_code(code)
            if not link:
                return {'error': 'link not found'}, 404
            return {'link': link.original_link}
        id_lst = data.get('id_lst')
        print(id_lst)
        links = Link.get_links_by_id(id_lst)
        host = request.host
        links = [link.to_json(host) for link in links]
        return {'links': links}




if __name__ == '__main__':

    app.run()
