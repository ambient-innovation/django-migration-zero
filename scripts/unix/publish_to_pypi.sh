#!/bin/bash
uv build
uv publish --publish-url https://test.pypi.org/legacy/
uv publish
