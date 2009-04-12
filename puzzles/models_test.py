import os
import unittest
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import user_service_stub
from google.appengine.api import users

from google.appengine.ext.db import BadValueError
from google.appengine.ext import db

from puzzles.models import *

class GAEModelTest(unittest.TestCase):
  def setUp(self):
    # Preserve the current apiproxy for tearDown().
    self.original_apiproxy = apiproxy_stub_map.apiproxy

    # Create a new apiproxy and temporary datastore that will be used for this test.
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    temp_stub = datastore_file_stub.DatastoreFileStub('AppEngineTestCaseDataStore', None, None)
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', temp_stub)

    apiproxy_stub_map.apiproxy.RegisterStub('user', user_service_stub.UserServiceStub())
    os.environ['AUTH_DOMAIN'] = 'gmail.com'
    os.environ['USER_EMAIL'] = 'myself@appengineguy.com' # set to '' for no logged in user
    os.environ['SERVER_NAME'] = 'fakeserver.com'
    os.environ['SERVER_PORT'] = '9999'

    # For convenience, the subclass can implement 'set_up' rather than overriding setUp()
    # and calling this base method.
    if hasattr(self, 'set_up'):
      self.set_up()

  def tearDown(self):
    # The subclass can optionally choose to implement 'tear_down'.
    if hasattr(self, 'tear_down'):
      self.tear_down()

    # Restore stubs for development.
    apiproxy_stub_map.apiproxy = self.original_apiproxy

class PuzzleTest(GAEModelTest):

  def test_puzzleValidation(self):
    self.assertRaises(BadValueError, Puzzle)

  def test_puzzle_getAbsoluteUrl(self):
    puzzle = Puzzle(title="title", description="description")
    key = puzzle.put()
    expected = db.get(key)
    self.assertEqual("/puzzle/"+ str(expected.key().id()) +"/view", expected.get_absolute_url())

class SolutionTest(GAEModelTest):

  def test_solution_validation(self):
    self.assertRaises(BadValueError, Solution)
    self.assertRaises(BadValueError, lambda x=1: Solution(title="title", detail="description"))

  def test_solution_getAbsoluteUrl(self):
    puzzle = Puzzle(title="title", description="description")
    puzzle_key = puzzle.put()
    solution = Solution(title="title", code="description", formatted_code="formatted", puzzle=puzzle, language="scala")
    key = solution.put()
    expected = db.get(key)
    self.assertEqual("/puzzle/"+ str(puzzle.key().id()) + "/solution/" + str(expected.key().id()) + "/view",
        expected.get_absolute_url())

class Solution_To_Puzzle_Test(GAEModelTest):

  def set_up(self):
    self.puzzle = Puzzle(title="title", description="description")
    puzzle_key = self.puzzle.put()
    self.solution = Solution(title="title", detail="description", puzzle=self.puzzle, language="scala", code="code")
    key = self.solution.put()
    self.puzzle = Puzzle.get_by_id(int(puzzle_key.id()))
    self.solution = Solution.get_by_id(int(key.id()))

  def test_puzzle_sol_references(self):
    self.failIf(self.puzzle.solution_set.count() <> 1)
    self.assertEqual(self.puzzle.key(), self.solution.puzzle.key())

if __name__ == "__main__":
  unittest.main()

