#!/bin/bash
uv build
uv publish --publish-url https://test.pypi.org/legacy/ --username __token__
uv publish --username __token__
