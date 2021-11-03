#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def setUp(self):
        """Set up for the doc tests"""
        self.state_1 = State(name="EstadoDePrueba")
        self.state_1.save()
        self.city_1 = City(name="CiudadDePrueba", state_id=self.state_1.id, )
        self.city_1.save()
        self.user_1 = User(email="a@a", password="123")
        self.user_1.save()
        self.place_1 = Place(name="Place de prueba 1", city_id=self.city_1.id,
                             user_id=self.user_1.id, number_rooms=3,
                             number_bathrooms=2, max_guest=3,
                             price_by_night=100)
        self.place_1.save()
        self.amenity_1 = Amenity(name="Internet")
        self.amenity_1.save()
        self.review_1 = Review(text="Review de prueba",
                               place_id=self.place_1.id,
                               user_id=self.user_1.id)
        self.review_1.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all(self):
        """Tests if returns the right quantity of elements"""
        num_objs = storage.count()
        new_obj = State(name="EstadoDePrueba 2")
        new_obj.save()
        new_num_objs = storage.count()
        self.assertEqual(num_objs, new_num_objs - 1, "Count not equal")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_state(self):
        """Tests if returns the right quantity of elements"""
        num_objs = storage.count(State)
        new_obj = State(name="EstadoDePrueba")
        new_obj.save()
        new_num_objs = storage.count(State)
        self.assertEqual(num_objs, new_num_objs - 1, "Count not equal")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_city(self):
        """Tests if returns the right quantity of elements"""
        num_objs = storage.count(City)
        new_obj = City(name="CiudadDePrueba", state_id=self.state_1.id)
        new_obj.save()
        new_num_objs = storage.count(City)
        self.assertEqual(num_objs, new_num_objs - 1, "Count not equal")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_amenity(self):
        """Tests if returns the right quantity of elements"""
        num_objs = storage.count(Amenity)
        new_obj = Amenity(name="WiFi")
        new_obj.save()
        new_num_objs = storage.count(Amenity)
        self.assertEqual(num_objs, new_num_objs - 1, "Count not equal")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_review(self):
        """Tests if returns the right quantity of elements"""
        num_objs = storage.count(Review)
        new_obj = Review(text="Review prueba", user_id=self.user_1.id,
                         place_id=self.place_1.id)
        new_obj.save()
        new_num_objs = storage.count(Review)
        self.assertEqual(num_objs, new_num_objs - 1, "Count not equal")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_place(self):
        """Tests if returns the right quantity of elements"""
        num_objs = storage.count(Place)
        new_obj = Place(name="Place De Prueba", city_id=self.city_1.id,
                        user_id=self.user_1.id, number_rooms=3,
                        number_bathrooms=1, max_guest=5,
                        price_by_night=150)
        new_obj.save()
        new_num_objs = storage.count(Place)
        self.assertEqual(num_objs, new_num_objs - 1, "Count not equal")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_user(self):
        """Tests if returns the right quantity of elements"""
        num_objs = storage.count(User)
        new_obj = User(name="User de prueba", email="b@b", password="abc")
        new_obj.save()
        new_num_objs = storage.count(User)
        self.assertEqual(num_objs, new_num_objs - 1, "Count not equal")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_state(self):
        """Tests if returns the right obj with the given id"""
        first_state_obj = list(storage.all(State).values())[0]
        first_state_id = first_state_obj.id
        obj = storage.get(State, first_state_id)
        self.assertIs(first_state_obj, obj, "Obj retrieved is not right")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_city(self):
        """Tests if returns the right obj with the given id"""
        first_city_obj = list(storage.all(City).values())[0]
        first_city_id = first_city_obj.id

        obj = storage.get(City, first_city_id)
        self.assertIs(first_city_obj, obj, "Obj retrieved is not right")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_amenity(self):
        """Tests if returns the right obj with the given id"""
        first_amenity_obj = list(storage.all(Amenity).values())[0]
        first_amenity_id = first_amenity_obj.id
        obj = storage.get(Amenity, first_amenity_id)
        self.assertIs(first_amenity_obj, obj, "Obj retrieved is not right")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_review(self):
        """Tests if returns the right obj with the given id"""
        first_review_obj = list(storage.all(Review).values())[0]
        first_review_id = first_review_obj.id
        obj = storage.get(Review, first_review_id)
        self.assertIs(first_review_obj, obj, "Obj retrieved is not right")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_place(self):
        """Tests if returns the right obj with the given id"""
        first_place_obj = list(storage.all(Place).values())[0]
        first_place_id = first_place_obj.id
        obj = storage.get(Place, first_place_id)
        self.assertIs(first_place_obj, obj, "Obj retrieved is not right")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_user(self):
        """Tests if returns the right obj with the given id"""
        first_user_obj = list(storage.all(User).values())[0]
        first_user_id = first_user_obj.id
        obj = storage.get(User, first_user_id)
        self.assertIs(first_user_obj, obj, "Obj retrieved is not right")
