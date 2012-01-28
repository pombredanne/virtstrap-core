from cStringIO import StringIO
import textwrap
import fudge
from nose.tools import raises
from virtstrap.exceptions import RequirementsConfigError
from virtstrap.requirements import *

TEST_REQUIREMENTS_YML = """
requirements:
  - ipython
  - jinja2:
    - https://github.com/mitsuhiko/jinja2.git
    - editable: true
  - werkzeug: '==0.8'
  - requests: '>=0.8'
"""

def test_initialize_processor():
    processor = RequirementSet()

def test_initialize_from_data():
    processor = RequirementSet.from_raw_data([])
    assert isinstance(processor, RequirementSet)

class TestRequirementSet(object):
    """RequirementSet test without mocks"""

    def setup(self):
        self.processor = RequirementSet()

    def test_create_requirements_file(self):
        # Define a requirements list
        requirements_list = [
            'ipython',
            {'werkzeug': '==0.8'},
            {'requests': '>=0.8'},
            {'jinja2': [
                'git+https://github.com/mitsuhiko/jinja2.git',
                {'editable': True},
            ]}
        ]
        # Define the expected created file
        expected_string = textwrap.dedent("""
            ipython
            werkzeug==0.8
            requests>=0.8
            -e git+https://github.com/mitsuhiko/jinja2.git#egg=jinja2
        """).strip()
        self.processor.set_requirements(requirements_list)
        
        pip_str = self.processor.to_pip_str()

        assert pip_str == expected_string

    @raises(RequirementsConfigError)
    def test_badly_configured_requirements(self):
        """Test that an error is thrown when there is a bad requirement"""
        requirements_list = [
            {'somereq': 'version', 'other': 'version'},
        ]
        self.processor.set_requirements(requirements_list)

        fake_file = fudge.Fake().is_a_stub()

        self.processor.to_pip_str()

def test_initialize_requirement_object():
    requirement = Requirement('somename')
    
def test_requirement_to_pip_string():
    requirement = Requirement('test')
    assert requirement.to_pip_str() == 'test'

def test_requirement_to_pip_string_with_version():
    requirement = Requirement('test', version='==0.9')
    assert requirement.to_pip_str() == 'test==0.9'

def test_requirement_to_pip_string_with_multiple_version_specs():
    requirement = Requirement('test', version='>=0.9,<1.5')
    assert requirement.to_pip_str() == 'test>=0.9,<1.5'

def test_vcs_requirement_to_pip_string():
    requirement = VCSRequirement('test', 'git+http://test.com/')
    assert requirement.to_pip_str() == 'git+http://test.com/#egg=test'

def test_vcs_requirement_to_pip_string_with_editable_flag():
    requirement = VCSRequirement('test', 'git+http://test.com/', editable=True)
    assert requirement.to_pip_str() == '-e git+http://test.com/#egg=test'

def test_vcs_requirement_to_pip_string_with_at_option():
    """Test that you can specify a tag, version, or commit"""
    requirement = VCSRequirement('test', 'git+http://test.com/', at="v1.0", 
            editable=True)
    assert requirement.to_pip_str() == '-e git+http://test.com/@v1.0#egg=test'