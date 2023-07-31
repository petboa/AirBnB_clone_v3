#!/usr/bin/python3
"""
Handle all amenity requests
"""
import models
import os
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_place_amenities(place_id):
    """get all amenities in a place"""
    if models.storage_t == 'db':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = []
        for amenity in storage.all(Amenity).values():
            if amenity.place_id == place_id:
                amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False)
def get_place_amenity(place_id, amenity_id):
    """get an amenity"""
    if models.storage_t == 'db':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                return jsonify(amenity.to_dict())
        abort(404)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None or amenity.place_id != place_id:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity object from a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """create an amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(404, 'Missing name')
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenityto_dict()), 201)
