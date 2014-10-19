from nose.tools import assert_raises, assert_dict_equal
from gravier import url_parse

class TestUrlParse():

    def setUp(self):
        self.https_url = 'https://www.sec.gov/cgi-bin/browse-edgar?company=Carrizo&owner=exclude&action=getcompany'
        self.http_url = 'http://www.sec.gov/cgi-bin/browse-edgar?company=Carrizo&owner=exclude&action=getcompany'
        self.http_url_encoded = 'http%3A%2F%2Fwww.sec.gov%2Fcgi-bin%2Fbrowse-edgar%3Fcompany%3DCarrizo%26owner%3Dexclude%26action%3Dgetcompany'

        self.url_ending_in_host = 'http://www.sec.gov'
        self.url_ending_in_port = 'http://www.sec.gov:6080'
        self.url_ending_in_path = 'http://www.sec.gov:6080/cgi-bin/browse-edgar'
        self.url_ending_in_query = 'http://www.sec.gov:6080/cgi-bin/browse-edgar?company=Carrizo&owner=exclude&action=getcompany'
        self.url_ending_in_fragment = 'https://www.sec.gov:6080/cgi-bin/browse-edgar#home'
        self.url_no_protocol = 'www.sec.gov:6080/cgi-bin/browse-edgar?company=Carrizo&owner=exclude&action=getcompany'

        self.correct_query_params = {}
        self.correct_query_params['company'] = 'Carrizo'
        self.correct_query_params['owner'] = 'exclude'
        self.correct_query_params['action'] = 'getcompany'

    def test_match_protocol(self):
        correct_protocol = 'http'
        assert url_parse.match_protocol(self.url_ending_in_host) == correct_protocol
        assert url_parse.match_protocol(self.url_ending_in_port) == correct_protocol
        assert url_parse.match_protocol(self.https_url) == 'https'
        assert url_parse.match_protocol(self.url_no_protocol) == None

    def test_match_host(self):
        correct_host = 'www.sec.gov'
        assert url_parse.match_host(self.url_ending_in_host) == correct_host
        assert url_parse.match_host(self.url_ending_in_port) == correct_host

    def test_match_port(self):
        correct_port = 6080
        assert url_parse.match_port(self.url_ending_in_port) == correct_port
        assert url_parse.match_port(self.url_ending_in_query) == correct_port
        assert url_parse.match_port(self.url_ending_in_host) == None

    def test_match_path(self):
        correct_path = '/cgi-bin/browse-edgar'
        assert url_parse.match_path(self.url_ending_in_path) == correct_path
        assert url_parse.match_path(self.url_ending_in_fragment) == correct_path
        assert url_parse.match_path(self.url_ending_in_query) == correct_path

    def test_match_query(self):
        query_params = url_parse.match_query(self.url_ending_in_query)
        assert_dict_equal(query_params, self.correct_query_params)

        query_params = url_parse.match_query(self.url_ending_in_query)
        assert_dict_equal(query_params, self.correct_query_params)

    def test_parsed_url_instantiation(self):
        url_obj = url_parse.ParsedURL(self.http_url_encoded)
        
        assert hasattr(url_obj, 'protocol')
        assert isinstance(url_obj.protocol, str)

        assert hasattr(url_obj, 'host')
        assert isinstance(url_obj.host, str)

        assert hasattr(url_obj, 'query')
        assert isinstance(url_obj.query, dict)

        assert hasattr(url_obj, 'port')
        assert isinstance(url_obj.port, int)

        assert hasattr(url_obj, 'fragment')
        assert isinstance(url_obj.fragment, str)

        assert hasattr(url_obj, 'path')
        assert isinstance(url_obj.path, str)

    def test_throw_error_on_invalid_url(self):
        assert_raises(ValueError, url_parse.ParsedURL, "jar jar binks")
