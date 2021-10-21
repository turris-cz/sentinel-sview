import pytest

from pwned.utils import compose_message, unfold_pg_array


def test_outgoing_validate(capsys):
    """Test validation of outgoing message."""
    compose_message("SUCCESS", {"hello": "World"})
    _, err = capsys.readouterr()
    assert "is not of type 'array'" in err


@pytest.mark.parametrize(
    "sources",
    [
        ("{ftp,http,smtp,telnet,haas}", ["ftp", "http", "smtp", "telnet", "haas"]),
        ("{haas,smtp}", ["haas", "smtp"]),
        ("{telnet,ftp}", ["telnet", "ftp"]),
    ],
)
def test_unfold_pg_array(sources):
    array = unfold_pg_array(sources[0])
    assert array == sources[1]
