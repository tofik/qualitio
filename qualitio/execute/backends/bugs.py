import httplib2
from xml.dom import pulldom
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

class IssueError(Exception):
    pass


class IssueServerError(Exception):
    pass


class Bugzilla(httplib2.Http):
    resource = None
    url = ""

    @classmethod
    def _setup_connection(cls):
        if hasattr(settings, "ISSUE_BACKEND_BUGZILLA_URL"):
            cls.url = settings.ISSUE_BACKEND_BUGZILLA_URL.rstrip("/")
        else:
            raise ImproperlyConfigured("Bugzill issue backed requires ISSUE_BACKEND_BUGZILLA_URL value in settings")

        login = getattr(settings, "ISSUE_BACKEND_BUGZILLA_USER", "")
        password = getattr(settings, "ISSUE_BACKEND_BUGZILLA_PASSWORD", "")
        cls.resource = httplib2.Http()
        if login:
            cls.resource.add_credentials(login, password)

    @classmethod
    def fetch_bug(cls, bug_id):
        if not cls.resource:
            cls._setup_connection()
        try:
            resp, content = cls.resource.request(
                "%s/show_bug.cgi?id=%s&ctype=xml" % (cls.url, bug_id))

        except httplib2.ServerNotFoundError, e:
            raise IssueServerError(e)
        if resp['status'] == "200":
            return cls._parse_response(content)
        raise IssueServerError(
            u"Unable to connect the server at %s, status code %s" %
            (cls.url, resp['status']))

    @classmethod
    def _parse_response(self, content):
        bugs = {}
        stream = pulldom.parseString(content)
        for (event, node) in stream:
            if event == "START_ELEMENT" and node.tagName == "bug":
                stream.expandNode(node)
                error = node.getAttribute("error")
                if error:
                    raise IssueError(error)

                bugs['id'] = node.getElementsByTagName("bug_id")[0].firstChild.data
                bugs['name'] = node.getElementsByTagName("short_desc")[0].firstChild.data
                bugs['status'] = node.getElementsByTagName("bug_status")[0].firstChild.data
                bugs['resolution'] = node.getElementsByTagName("resolution") or ""
                if bugs['resolution']:
                    bugs['resolution'] = bugs['resolution'][0].firstChild.data

        return bugs


class RemoteBugManager(models.Manager):

    def _update_query_set(self, query):
        for bug in query:
            try:
                bug_dict = Bugzilla.fetch_bug(bug.id)
                bug.name = bug_dict['name']
                bug.status = bug_dict['status']
                bug.resolution = bug_dict['resolution']
                bug.save()
            except IssueError:
                pass

        return query


    def _update_object(self, bug):
        try:
            bug_dict = Bugzilla.fetch_bug(bug.id)
            bug.name = bug_dict['name']
            bug.status = bug_dict['status']
            bug.resolution = bug_dict['resolution']
            bug.save()
        except IssueError:
            pass

        return bug


    def all(self):
        return self.get_query_set()


    def get(self, *args, **kwargs):
        try:
            query = self.get_query_set().get(*args, **kwargs)
            return self._update_object(query)
        except self.model.DoesNotExist:
            if "id" in kwargs:
                try:
                    return self.remote_get(kwargs['id'])
                except IssueError, e:
                    raise self.model.DoesNotExist(e)
            else:
                raise self.model.DoesNotExist


    def remote_get(self, id):
        bug_dict = Bugzilla.fetch_bug(id)
        return self.model.objects.create(id = bug_dict['id'],
                                         name = bug_dict['name'],
                                         status = bug_dict['status'],
                                         resolution = bug_dict['resolution'])
