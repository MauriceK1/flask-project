#!/bin/sh

pip install mutpy
mut.py --target app.app --unit-test tests.test_db --runner unittest
mut.py --target app.app --unit-test tests.test_app --runner unittest