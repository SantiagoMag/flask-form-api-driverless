# Flask Service for REST Connections to Multiple Servers

This repository contains a Flask-based web service that connects to multiple servers via REST API. The service enables seamless integration with various machine learning server instances, providing endpoints for connecting to different predictive models.

## Branch Structure

- **Main Branch**: Contains the API implementation for connecting to **Driverless AI**. This branch provides specific endpoints to send data and receive predictions from machine learning models hosted on a Driverless AI instance.

- **Azure Branch**: This branch is configured to connect to an **Azure instance** with a deployed machine learning model. It uses a REST API to exchange data with the model hosted on Azure.

## Building the Executable

To create a standalone `.exe` file for the application, use the following `cmd` command with `pyinstaller`:

```cmd
pyinstaller --onefile --noconsole --hidden-import=pyodbc --add-data "app/templates:app/templates" --add-data "app/static:app/static" --add-data "app/forms:app/forms" --add-data "app/models:app/models" --add-data "app/routes:app/routes" --add-data "uploads:uploads" --name DemoAPI-ML run.py
