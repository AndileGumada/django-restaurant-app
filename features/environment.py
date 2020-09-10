"""
This file defines the Django settings to load and test,
the context to be passed to each testing step, and then what to
"""
import os
import django
from behave.runner import Context
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.shortcuts import resolve_url
from django.test.runner import DiscoverRunner
from splinter.browser import Browser

os.environ["DJANGO_SETTINGS_MODULE"] = "myrecommendations.settings"

class ExtendedContext(Context):
    def get_url(self, to=None, *args, **kwargs):
        return self.test.live_server_url + (
            resolve_url(to, *args, **kwargs) if to else '')

"""
 setting Django, preparing it for testing and a 
 browser session based on PhantomJS to act as the user.
"""

def before_all(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.browser = Browser('chrome', headless=True)

"""
The Django database is initialized, together with the context to be passed to
 each scenario step implementation with all the data about the current application status.
"""
def before_scenario(context, scenario):
    context.test_runner.setup_databases()
    object.__setattr__(context, '__class__', ExtendedContext)
    context.test = StaticLiveServerTestCase
    context.test.setUpClass()

"""
The Django database is destroyed so the next scenario will start with a clean one.
This way each scenario is independent from previous ones and interferences are avoided.
"""
def after_scenario(context, scenario):
    context.test.tearDownClass()
    del context.test
    call_command('flush', verbosity=0, interactive=False)
"""
The testing environment is destroyed together with the browser used for testing.
"""
def after_all(context):
    context.test_runner.teardown_test_environment()
    context.browser.quit()
    context.browser = None
