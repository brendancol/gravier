gravier
=======

Utilities for common tasks encountered in the wild web (under construction)
[![Build Status](https://travis-ci.org/brendancol/gravier.svg)](https://travis-ci.org/brendancol/gravier)


### Notes: 
	1. Currently only contains simple url parser (url_parse module)
	2. Requires Python 3.4+ (brew install python3)

### Setup environment (OSX / *nix):
    $> git clone https://github.com/brendancol/gravier.git
    $> cd gravier
    $> pyvenv env && source env/bin/activate
    $> pip install -r requirements.txt

### Run tests
    $> nosetests -v

       tests.test_url_parse.TestUrlParse.test_match_host ... ok
       tests.test_url_parse.TestUrlParse.test_match_path ... ok
       tests.test_url_parse.TestUrlParse.test_match_port ... ok
       tests.test_url_parse.TestUrlParse.test_match_protocol ... ok
       tests.test_url_parse.TestUrlParse.test_match_query ... ok
       tests.test_url_parse.TestUrlParse.test_parsed_url_instantiation ... ok
       tests.test_url_parse.TestUrlParse.test_throw_error_on_invalid_url ... ok