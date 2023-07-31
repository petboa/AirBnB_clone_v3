#!/usr/bin/python3
"""
handles the places requests
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage as s
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                                  strict_slashes=False)
def places(city_id):
        """gets places of a city"""
            city = s.get("City", city_id)
                if city is None:
                            abort(404)
                                places = []
                                    for place in city.places:
                                                places.append(place.to_dict())
                                                    return jsonify(places)


                                                @app_views.route('/places/<string:place_id>', methods=['GET'],
                                                                                  strict_slashes=False)
                                                def place(place_id):
                                                        """gets a place"""
                                                            place = s.get("Place", place_id)
                                                                if place is None:
                                                                            abort(404)
                                                                                return jsonify(place.to_dict())


                                                                            @app_views.route('/places/<string:place_id>', methods=['DELETE'],
                                                                                                              strict_slashes=False)
                                                                            def delete_place(place_id):
                                                                                    """deletes a place"""
                                                                                        place = s.get("Place", place_id)
                                                                                            if place is None:
                                                                                                        abort(404)
                                                                                                            place.delete()
                                                                                                                s.save()
                                                                                                                    return (jsonify({}))


                                                                                                                @app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                                                                                                                                                  strict_slashes=False)
                                                                                                                def create_place(city_id):
                                                                                                                        """create a new place"""
                                                                                                                            city = s.get("City", city_id)
                                                                                                                                if city is None:
                                                                                                                                            abort(404)
                                                                                                                                                if not request.get_json():
                                                                                                                                                            return make_response(jsonify({'error': 'Not a JSON'}), 400)
                                                                                                                                                            dict = request.get_json()
                                                                                                                                                                if 'user_id' not in dict:
                                                                                                                                                                            return make_response(jsonify({'error': 'Missing user_id'}), 400)
                                                                                                                                                                            user = s.get("User", dict['user_id'])
                                                                                                                                                                                if user is None:
                                                                                                                                                                                            abort(404)
                                                                                                                                                                                                if 'name' not in dict:
                                                                                                                                                                                                    ~
