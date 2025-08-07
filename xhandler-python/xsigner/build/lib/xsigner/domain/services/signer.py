from lxml import etree
import xmlsec

class Signer:
    def sign(self, xml_content: str, key_file: str, cert_file: str) -> str:
        # Parse the XML
        root = etree.fromstring(xml_content.encode("utf-8"))

        # Find the UBLExtensions element
        ubl_extensions = root.find("{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}UBLExtensions")
        if ubl_extensions is None:
            raise ValueError("UBLExtensions element not found in the XML")

        # Create the signature template
        signature = xmlsec.template.create(
            root,
            xmlsec.constants.TransformExclC14N,
            xmlsec.constants.TransformRsaSha256,
        )

        # Add the signature to the UBLExtensions
        ubl_extensions.append(signature)

        # Add a reference to the document
        ref = xmlsec.template.add_reference(
            signature, xmlsec.constants.TransformSha256, uri=""
        )
        xmlsec.template.add_transform(ref, xmlsec.constants.TransformEnveloped)

        # Add key info and X509 data
        key_info = xmlsec.template.ensure_key_info(signature)
        xmlsec.template.add_x509_data(key_info)

        # Sign the XML
        ctx = xmlsec.SignatureContext()
        ctx.key = xmlsec.Key.from_file(key_file, xmlsec.constants.KeyDataFormatPem)
        ctx.key.load_cert_from_file(cert_file, xmlsec.constants.KeyDataFormatPem)
        ctx.sign(signature)

        # Return the signed XML as a string
        return etree.tostring(root, encoding="utf-8").decode("utf-8")
