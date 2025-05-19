import pytest
import tempfile
from pathlib import Path
from textwrap import dedent

from app.data_accessor.pandas.company_handler import CompanyHandler
from app.data_models.company import Company

@pytest.fixture
def company_csv_file() -> Path:
    content = dedent("""
        company_id,company_name,company_email
        1,Acme Corp,hello@acme.com
        2,Initech,contact@initech.com
    """)
    # create a NamedTemporaryFile that persists after closing
    tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv')
    try:
        tmp.write(content)
        tmp.flush()
        return Path(tmp.name)
    finally:
        tmp.close()

@pytest.fixture(autouse=True)
def cleanup_file(company_csv_file):
    yield
    try:
        company_csv_file.unlink()
    except Exception:
        pass

def test_get_by_id_exists(company_csv_file):
    handler = CompanyHandler(company_csv_file)
    company = handler.get_by_id(2)

    assert isinstance(company, Company)
    assert company.company_id == 2
    assert company.company_name == "Initech"

def test_get_by_id_not_exists(company_csv_file):
    handler = CompanyHandler(company_csv_file)
    assert handler.get_by_id(999) is None

def test_get_company_from_company_name_exists(company_csv_file):
    handler = CompanyHandler(company_csv_file)
    company = handler.get_company_from_company_name("Acme Corp")

    assert isinstance(company, Company)
    assert company.company_id == 1
    assert company.company_name == "Acme Corp"

def test_get_company_from_company_name_not_exists(company_csv_file):
    handler = CompanyHandler(company_csv_file)
    assert handler.get_company_from_company_name("Nonexistent Co") is None
