from nose.tools import assert_raises, assert_dict_equal
from gravier import url_parse

class TestUrlParse():

    def setUp(self):
        self.url_https = 'https://www.sec.gov/cgi-bin/browse-edgar?company=Carrizo&owner=exclude&action=getcompany'
        self.url_http = 'http://www.sec.gov/cgi-bin/browse-edgar?company=Carrizo&owner=exclude&action=getcompany'
        self.url_encoded = 'http%3A%2F%2Fwww.sec.gov%2Fcgi-bin%2Fbrowse-edgar%3Fcompany%3DCarrizo%26owner%3Dexclude%26action%3Dgetcompany'
        self.url_ending_in_host = 'http://www.sec.gov'
        self.url_ending_in_html = 'http://www.sec.gov/index.html'
        self.url_ending_in_port = 'http://www.sec.gov:6080'
        self.url_ending_in_path = 'http://www.sec.gov:6080/cgi-bin/browse-edgar'
        self.url_ending_in_query = 'http://www.sec.gov:6080/cgi-bin/browse-edgar?company=Carrizo&owner=exclude&action=getcompany'
        self.url_ending_in_fragment = 'https://www.sec.gov:6080/cgi-bin/browse-edgar#home'
        self.url_no_protocol = 'www.sec.gov:6080/cgi-bin/browse-edgar?company=Carrizo&owner=exclude&action=getcompany'

        self.correct_protocol = 'http'
        self.correct_host = 'www.sec.gov'
        self.correct_port = 6080
        self.correct_path = '/cgi-bin/browse-edgar'
        self.correct_query_params = {}
        self.correct_query_params['company'] = 'Carrizo'
        self.correct_query_params['owner'] = 'exclude'
        self.correct_query_params['action'] = 'getcompany'

    def test_match_protocol(self):
        assert url_parse.match_protocol(self.url_ending_in_host) == self.correct_protocol 
        assert url_parse.match_protocol(self.url_ending_in_port) == self.correct_protocol 
        assert url_parse.match_protocol(self.url_ending_in_html) == self.correct_protocol 
        
    def test_https_protocol(self):
        assert url_parse.match_protocol(self.url_https) == 'https'

    def test_handle_no_protocol(self):
        assert url_parse.match_protocol(self.url_no_protocol) == None

    def test_match_host(self):
        assert url_parse.match_host(self.url_ending_in_host) == self.correct_host
        assert url_parse.match_host(self.url_ending_in_port) == self.correct_host
        assert url_parse.match_host(self.url_ending_in_html) == self.correct_host

    def test_match_port(self):
        assert url_parse.match_port(self.url_ending_in_port) == self.correct_port
        assert url_parse.match_port(self.url_ending_in_query) == self.correct_port
        
    def test_match_default_port_80(self):
        assert url_parse.match_port(self.url_ending_in_html) == 80
        assert url_parse.match_port(self.url_ending_in_host) == 80

    def test_match_path(self):
        correct_path = '/cgi-bin/browse-edgar'
        assert url_parse.match_path(self.url_ending_in_path) == self.correct_path
        assert url_parse.match_path(self.url_ending_in_fragment) == self.correct_path
        assert url_parse.match_path(self.url_ending_in_query) == self.correct_path

    def test_index_html_path(self):
        assert url_parse.match_path(self.url_ending_in_html) == '/index.html'

    def test_match_query(self):
        query_params = url_parse.match_query(self.url_ending_in_query)
        assert_dict_equal(query_params, self.correct_query_params)

        query_params = url_parse.match_query(self.url_ending_in_query)
        assert_dict_equal(query_params, self.correct_query_params)

    def test_parsed_url_instantiation(self):
        url_obj = url_parse.ParsedURL(self.url_encoded)

        assert hasattr(url_obj, 'protocol')
        assert isinstance(url_obj.protocol, str)
        assert url_obj.protocol == self.correct_protocol

        assert hasattr(url_obj, 'host')
        assert isinstance(url_obj.host, str)
        assert url_obj.host == self.correct_host

        assert hasattr(url_obj, 'query')
        assert isinstance(url_obj.query, dict)
        assert_dict_equal(url_obj.query, self.correct_query_params)

        assert hasattr(url_obj, 'port')
        assert isinstance(url_obj.port, int)
        assert url_obj.port == 80

        assert hasattr(url_obj, 'path')
        assert isinstance(url_obj.path, str)
        assert url_obj.path == self.correct_path

    def test_throw_error_on_invalid_url(self):
        assert_raises(ValueError, url_parse.ParsedURL, 'jar jar binks')
