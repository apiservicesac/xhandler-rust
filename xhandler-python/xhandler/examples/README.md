# xhandler-python Examples

This directory contains examples of how to use the `xhandler-python` library.

## Prerequisites

Before running the examples, make sure you have installed the necessary dependencies. From the root of the `xhandler-python/xhandler` directory, run:

```bash
uv pip install -e .
```

## Running the Examples

### Invoice Example

To run the invoice example, execute the following command from the `xhandler-python/xhandler/examples` directory:

```bash
python invoice_example.py
```

This script will:
1.  Create an `Invoice` object with sample data.
2.  Use the `Handler` to process the invoice.
3.  Connect to the SUNAT beta environment to send the invoice.
4.  Print the response from SUNAT.
5.  If successful, it will save the generated `invoice.zip` and the response `cdr.zip` in the current directory.

The example uses test credentials for the SUNAT beta environment. The `private.key` and `public.crt` files are also provided.

## Unsupported Features

As of now, the Python version of the `xbuilder` library does not support the creation of credit notes or debit notes. The necessary entities and rendering logic have not been implemented yet.
