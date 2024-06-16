import sys
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta, timezone
import os
import argparse

def create_ca(validity_days, key_size):
    ca_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
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
        now + timedelta(days=validity_days)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    ).sign(ca_private_key, hashes.SHA256(), default_backend())

    return ca_private_key, ca_cert

def create_server_certificate(cn, sans, ca_cert, ca_private_key, validity_days, key_size):
    server_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    now = datetime.now(timezone.utc)
    csr_builder = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "JP"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tokyo"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Minato"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Server Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
    ]))

    if sans:
        csr_builder = csr_builder.add_extension(
            x509.SubjectAlternativeName([x509.DNSName(san) for san in sans]),
            critical=False
        )

    csr = csr_builder.sign(server_private_key, hashes.SHA256(), default_backend())

    cert_builder = x509.CertificateBuilder().subject_name(
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
        now + timedelta(days=validity_days)
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )

    if sans:
        cert_builder = cert_builder.add_extension(
            x509.SubjectAlternativeName([x509.DNSName(san) for san in sans]),
            critical=False
        )

    server_cert = cert_builder.sign(ca_private_key, hashes.SHA256(), default_backend())

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

def main(cn, sans, validity_days, key_size):
    dir_path = cn  # ディレクトリ名をCNに基づいて設定
    ca_private_key, ca_cert = create_ca(validity_days, key_size)
    save_pem(dir_path, "ca_private_key.pem", ca_private_key)
    save_pem(dir_path, "ca_certificate.pem", ca_cert)

    server_private_key, server_cert, csr = create_server_certificate(cn, sans, ca_cert, ca_private_key, validity_days, key_size)
    save_pem(dir_path, "server_private_key.pem", server_private_key)
    save_pem(dir_path, "server_certificate.pem", server_cert)
    save_pem(dir_path, "server_csr.pem", csr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a CA and server certificate.")
    parser.add_argument("--cn", type=str, required=True, help="Common Name for the server certificate")
    parser.add_argument("--sans", nargs='*', type=str, help="Subject Alternative Names for the server certificate")
    parser.add_argument("--days", type=int, default=365, help="Validity period of the certificates in days (default: 365)")
    parser.add_argument("--key-size", type=int, default=4096, help="Key size for the RSA keys (default: 4096)")

    args = parser.parse_args()
    main(args.cn, args.sans, args.days, args.key_size)