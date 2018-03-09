"""
example_specifications.py

Copyright 2018 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import json

from apispec import APISpec
from flask import Flask, jsonify
from marshmallow import Schema, fields


class IntParamQueryString(object):
    def get_specification(self):
        return '''\
{
  "swagger": "2.0",
  "info": {
    "version": "1.0.0",
    "title": "Query String",
    "description": "foo"
  },
  "host": "w3af.org",
  "basePath": "/api",
  "schemes": [
    "https"
  ],
  "consumes": [
    "application/json"
  ],
  "produces": [
    "application/json"
  ],
  "paths": {
    "/pets": {
      "get": {
        "description": "Returns all pets from the system that the user has access to",
        "operationId": "findPets",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "description": "maximum number of results to return",
            "required": false,
            "type": "integer",
            "format": "int32"
          }
        ],
        "responses": {
          "200": {
            "description": "pet response",
            "schema": {
              "type": "array",
              "items": {
                "$ref": "#/definitions/Pet"
              }
            }
          }
        }
      }
    }
  },
  "definitions": {
    "Pet": {
      "type": "object",
      "required": [
        "id"
      ],
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64"
        }
      }
    }
  }
}
'''


class IntParamPath(object):
    def get_specification(self):
        spec = APISpec(
            title=self.__class__.__name__,
            version='1.0.0',
            plugins=(
                'apispec.ext.flask',
                'apispec.ext.marshmallow',
            ),
        )

        class PetParameter(Schema):
            pet_id = fields.Int()

        class PetSchema(Schema):
            id = fields.Int()
            name = fields.Str()

        app = Flask(__name__)

        @app.route('/pets/<int:pet_id>')
        def get_pet(pet_id):
            """A cute furry animal endpoint.
            ---
            get:
                description: Get a random pet
                parameters:
                    - in: path
                      schema: PetParameter
                responses:
                    200:
                        description: A pet to be returned
                        schema: PetSchema
            """
            return jsonify({})

        # Register entities and paths
        spec.definition('Pet', schema=PetSchema)
        spec.definition('PetParameter', schema=PetParameter, required=True)
        with app.test_request_context():
            spec.add_path(view=get_pet)

        specification_as_string = json.dumps(spec.to_dict(), indent=4)

        # Kludge! I was unable to do this via `apispec`
        specification_as_string = specification_as_string.replace('"required": false,',
                                                                  '"required": true,')

        return specification_as_string


class StringParam(object):
    pass


class ArrayStringItems(object):
    pass


class ArrayIntItems(object):
    pass


class ArrayModelItems(object):
    pass


class NoParams(object):

    def get_specification(self):
        spec = APISpec(
            title=self.__class__.__name__,
            version='1.0.0',
            plugins=(
                'apispec.ext.flask',
                'apispec.ext.marshmallow',
            ),
        )

        class PetSchema(Schema):
            id = fields.Int()
            name = fields.Str()

        app = Flask(__name__)

        @app.route('/random')
        def random_pet():
            """A cute furry animal endpoint.
            ---
            get:
                description: Get a random pet
                responses:
                    200:
                        description: A pet to be returned
                        schema: PetSchema
            """
            return jsonify({})

        # Register entities and paths
        spec.definition('Pet', schema=PetSchema)
        with app.test_request_context():
            spec.add_path(view=random_pet)

        return json.dumps(spec.to_dict(), indent=4)


class ModelParam(object):

    def get_specification(self):
        spec = APISpec(
            title=self.__class__.__name__,
            version='1.0.0',
            plugins=(
                'apispec.ext.flask',
                'apispec.ext.marshmallow',
            ),
        )

        class PetSchema(Schema):
            id = fields.Int()
            name = fields.Str()

        app = Flask(__name__)

        @app.route('/random')
        def random_pet():
            """A cute furry animal endpoint.
            ---
            get:
                description: Get a random pet
                responses:
                    200:
                        description: A pet to be returned
                        schema: PetSchema
            """
            return jsonify({})

        # Register entities and paths
        spec.definition('Pet', schema=PetSchema)
        with app.test_request_context():
            spec.add_path(view=random_pet)

        return json.dumps(spec.to_dict(), indent=4)


class ModelParamNested(object):

    def get_specification(self):
        spec = APISpec(
            title=self.__class__.__name__,
            version='1.0.0',
            plugins=(
                'apispec.ext.flask',
                'apispec.ext.marshmallow',
            ),
        )

        class CategorySchema(Schema):
            id = fields.Int()
            name = fields.Str(required=True)

        class PetSchema(Schema):
            category = fields.Nested(CategorySchema, many=True)
            name = fields.Str()

        app = Flask(__name__)

        @app.route('/random')
        def random_pet():
            """A cute furry animal endpoint.
            ---
            get:
                description: Get a random pet
                responses:
                    200:
                        description: A pet to be returned
                        schema: PetSchema
            """
            return jsonify({})

        # Register entities and paths
        spec.definition('Category', schema=CategorySchema)
        spec.definition('Pet', schema=PetSchema)
        with app.test_request_context():
            spec.add_path(view=random_pet)

        return json.dumps(spec.to_dict(), indent=4)


class ModelParamNestedLoop(object):

    def get_specification(self):
        spec = APISpec(
            title=self.__class__.__name__,
            version='1.0.0',
            plugins=(
                'apispec.ext.flask',
                'apispec.ext.marshmallow',
            ),
        )

        class A(Schema):
            id = fields.Int()
            pointers = fields.Nested('B', many=True)

        class B(Schema):
            id = fields.Int()
            pointers = fields.Nested('C', many=True)

        class C(Schema):
            id = fields.Int()
            pointers = fields.Nested('A', many=True)

        app = Flask(__name__)

        @app.route('/random')
        def random_pet():
            """A cute furry animal endpoint.
            ---
            get:
                description: Get a random pet
                responses:
                    200:
                        description: A pet to be returned
                        schema: PetSchema
            """
            return jsonify({})

        # Register entities and paths
        spec.definition('A', schema=A)
        spec.definition('B', schema=B)
        spec.definition('C', schema=C)
        with app.test_request_context():
            spec.add_path(view=random_pet)

        return json.dumps(spec.to_dict(), indent=4)
