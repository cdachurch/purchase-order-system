""" Contains Test Fixtures for Google AppEngine dependencies """
from google.appengine.api.search.simple_search_stub import SearchServiceStub
import unittest
from datetime import datetime, timedelta
from webapp2 import cached_property
from minimock import Mock, mock, restore as minimock_restore
from google.appengine.ext import testbed
from google.appengine.api import urlfetch, datastore_types
from google.appengine.api.namespace_manager import get_namespace, set_namespace
from google.appengine.ext.testbed import TASKQUEUE_SERVICE_NAME

SEARCH_SERVICE_NAME = 'search'

class GaeTestCase(unittest.TestCase):
    """ Defines TestCase for testing App Engine code. See here for more info:
            http://code.google.com/appengine/docs/python/tools/localunittesting.html
    """

    def setUp(self):
        self._old_namespace = get_namespace()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub(_all_queues_valid=True)
        self.testbed.init_urlfetch_stub(enable=False)

    def tearDown(self):
        """ Tears down the test environment. """
        self.testbed.deactivate()
        minimock_restore()
        set_namespace(self._old_namespace)
        super(GaeTestCase, self).tearDown()

    def get_queued_tasks(self, queue_name='default'):
        taskqueue_stub = self.testbed.get_stub(TASKQUEUE_SERVICE_NAME)
        return taskqueue_stub.GetTasks(queue_name)

    def flush_queue(self, queue_name='default'):
        taskqueue_stub = self.testbed.get_stub(TASKQUEUE_SERVICE_NAME)
        taskqueue_stub.FlushQueue(queue_name)

    def mock_urlfetch(self):
        """ Mock appengine's urlfetch.
            self.response can then be modified to whatever urlfetch should return.
            self.response.raises will be raised to whichever exception it is set to.

            Instructions:
                Call self.mock_urlfetch() in setUp()
                Then self.response to whatever you want returned from the urlfetch for that test:
                    Eg. self.response.content = 'this is a urlfetch response'
                        self.response.raises = urlfetch.DownloadError

        """
        # disables urlfetch to ensure we don't inadvertently go over the wire
        self.testbed.init_urlfetch_stub(enable=False)

        self.response = UrlFetchResponseMock()

        # pylint: disable=E0702
        # Raising NoneType while only classes, instances or string are allowed
        # pylint: disable=W0613
        # Unused argument 'args' and 'kwargs'
        def fetch_mock(*args, **kwargs):
            if self.response.raises:
                raise self.response.raises
            return self.response
        
        # pylint: disable=W0612
        # Unused variable 'google'
        import google.appengine.api.urlfetch
        urlfetch.fetch = Mock('urlfetch.fetch', returns_func=fetch_mock, tracker=None)

    def run_deferred_tasks(self, queue_name='default'):
        import base64
        from google.appengine.ext import deferred
        tasks = self.get_queued_tasks(queue_name=queue_name)
        for task in tasks:
            deferred.run(base64.b64decode(task['body']))
        # flush tasks from queue after they are run
        self.flush_queue(queue_name=queue_name)

    def assertArgsAreRequired(self, method, **kwargs):
        """
        Asserts each of the arguments provided in kwargs are a required argument for the provided method.
        """
        for key, value in kwargs.iteritems():
            # test if arg is None
            kwargs[key] = None
            self.assertRaises(ValueError, method, **kwargs)
            # test if arg is empty string
            kwargs[key] = ""
            self.assertRaises(ValueError, method, **kwargs)
            # restore to original value
            kwargs[key] = value
