# from unittest import TestCase
# from app import app

# # class TestIntegrations(TestCase):
# #     def setUp(self):
# #         self.app = app.test_client()

# #     def test_thing(self):
# #         response = self.app.get('/')
# #         assert <make your assertion here>

# # from flask.ext.testing import TestCase

# class MyTest(TestCase):

#     def setUp(self):
#         self.app = app.test_client()

#     # def create_app(self):
#     #     return app

#     def test_greeting(self):
#         self.app.get('/')
#         print(self.app)
#         self.app.assert_template_used('index.html')