# SelfSignedCertGenerator

SelfSignedCertGenerator is a Python tool designed to automate the generation of self-signed Certificate Authorities (CAs) and server certificates. This tool helps developers quickly create CA certificates, server certificates, corresponding private keys, and Certificate Signing Requests (CSRs) for testing and development purposes.

## Features

- Generates a self-signed CA certificate.
- Uses the CA to sign server certificates.
- Creates corresponding private keys for the CA and server certificates.
- Generates a CSR for the server certificate.
- Easy to use with command line arguments for flexible certificate details.

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
git clone https://github.com/your-username/SelfSignedCertGenerator.git
cd SelfSignedCertGenerator
```

## Usage

Run the script from the command line, specifying the common name (CN) for the server certificate:

```bash
python generate-ca-and-certificate.py <common_name>
```

For example, to generate certificates for `example.com`:

```bash
python generate-ca-and-certificate.py example.com
```

This command will create a directory named after the CN, where all generated files (CA certificate, server certificate, private keys, and CSR) will be stored.

## Output

The following files will be generated in a directory named after your specified common name:

- `ca_certificate.pem` - The self-signed CA certificate.
- `server_certificate.pem` - The server certificate signed by your CA.
- `ca_private_key.pem` - Private key for the CA.
- `server_private_key.pem` - Private key for the server certificate.
- `server_csr.pem` - Certificate Signing Request for the server certificate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
