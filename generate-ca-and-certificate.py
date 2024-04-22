import sys
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta, timezone
import os

def create_ca():
    ca_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

    now = datetime.now(timezone.utc)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "JP"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tokyo"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Minato"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My CA Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, "My CA"),
    ])
    ca_cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        ca_private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        now
    ).not_valid_after(
        now + timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    ).sign(ca_private_key, hashes.SHA256(), default_backend())

    return ca_private_key, ca_cert

def create_server_certificate(cn, ca_cert, ca_private_key):
    server_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

    now = datetime.now(timezone.utc)
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "JP"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tokyo"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Minato"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Server Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
    ])).sign(server_private_key, hashes.SHA256(), default_backend())

    server_cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        now
    ).not_valid_after(
        now + timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    ).sign(ca_private_key, hashes.SHA256(), default_backend())

    return server_private_key, server_cert, csr

def save_pem(dir_path, file_name, data):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, "wb") as f:
        if isinstance(data, rsa.RSAPrivateKey):
            f.write(data.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=NoEncryption()
            ))
        elif isinstance(data, x509.Certificate):
            f.write(data.public_bytes(Encoding.PEM))
        elif isinstance(data, x509.CertificateSigningRequest):
            f.write(data.public_bytes(Encoding.PEM))
    print(f"File saved: {file_path}")

def main(cn):
    dir_path = cn
    ca_private_key, ca_cert = create_ca()
    save_pem(dir_path, "ca_private_key.pem", ca_private_key)
    save_pem(dir_path, "ca_certificate.pem", ca_cert)

    server_private_key, server_cert, csr = create_server_certificate(cn, ca_cert, ca_private_key)
    save_pem(dir_path, "server_private_key.pem", server_private_key)
    save_pem(dir_path, "server_certificate.pem", server_cert)
    save_pem(dir_path, "server_csr.pem", csr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <common_name>")
        sys.exit(1)
    cn = sys.argv[1]
    main(cn)
