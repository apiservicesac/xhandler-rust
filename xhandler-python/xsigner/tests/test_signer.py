import os
from lxml import etree
from xsigner.domain.services.signer import Signer

def test_signer_sign():
    # Arrange
    signer = Signer()
    xml_file = os.path.join(os.path.dirname(__file__), "sample.xml")
    key_file = os.path.join(os.path.dirname(__file__), "private.key")
    cert_file = os.path.join(os.path.dirname(__file__), "public.crt")

    with open(xml_file, "r") as f:
        xml_content = f.read()

    # Act
    signed_xml = signer.sign(xml_content, key_file, cert_file)

    # Assert
    root = etree.fromstring(signed_xml.encode("utf-8"))
    signature = root.find(".//{http://www.w3.org/2000/09/xmldsig#}Signature")
    assert signature is not None
