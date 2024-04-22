# SelfSignedCertGenerator

Quickly and simply generate your own CA and self-signed certificates with SelfSignedCertGenerator. This tool helps developers create CA certificates, server certificates, corresponding private keys, and Certificate Signing Requests (CSRs) for testing and development purposes, with support for Subject Alternative Names (SAN).

## Features

- Generates a self-signed CA certificate.
- Uses the CA to sign server certificates.
- Creates corresponding private keys for the CA and server certificates.
- Generates a CSR for the server certificate, including SANs.
- Easy to use with command line arguments for flexible certificate details, including multiple SAN entries.

## Customization

The script includes hardcoded values for certificate attributes such as COUNTRY_NAME, STATE_OR_PROVINCE_NAME, and others. If you need to change these values, you will need to modify the source code accordingly. Additionally, the default validity period for the CA and server certificates is set to 365 days, but this can be adjusted in the code as needed.

## Prerequisites

Ensure you have Python 3.6 or higher installed on your machine. You also need the `cryptography` library, which can be installed using pip:

```bash
pip install cryptography
```

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/knziiy/SelfSignedCertGenerator.git
cd SelfSignedCertGenerator
```

## Usage

Run the script from the command line, specifying the common name (CN) for the server certificate and any desired Subject Alternative Names (SANs):

```bash
python generate-ca-and-certificate.py <common_name> <san1> <san2> ...
```

For example, to generate certificates for `example.com` with additional SANs for `www.example.com` and `api.example.com`:

```bash
python generate-ca-and-certificate.py example.com www.example.com api.example.com
```

This command will create a directory named after the CN, where all generated files (CA certificate, server certificate, private keys, and CSR) will be stored. The server certificate will include the specified SANs.

## Output

The following files will be generated in a directory named after your specified common name:

- `ca_certificate.pem` - The self-signed CA certificate.
- `server_certificate.pem` - The server certificate signed by your CA, including all specified SANs.
- `ca_private_key.pem` - Private key for the CA.
- `server_private_key.pem` - Private key for the server certificate.
- `server_csr.pem` - Certificate Signing Request for the server certificate, including SANs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
