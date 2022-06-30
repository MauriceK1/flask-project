#!/bin/sh

pip install mutpy
# tests.test_db will create posts that show on the timeline page
mut.py --target app.app --unit-test tests.test_db --runner unittest
mut.py --target app.app --unit-test tests.test_app --runner unittest