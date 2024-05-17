#!/bin/bash
git clone -n --depth=1 --filter=tree:0 https://github.com/askui/askui-dev-docs.git documents_to_import
cd documents_to_import
git sparse-checkout set --no-cone docs/docs
git checkout

# Remove unwanted files
rm docs/docs/api/01-API/table-of-contents.md