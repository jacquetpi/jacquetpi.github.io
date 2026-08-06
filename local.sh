#!/bin/bash
# Build the site and serve the production output locally on http://localhost:8080
# (For development preview with live reload, use `hugo server` instead.)
hugo --minify && docker run --rm -p 8080:80 -v "$(pwd)/public:/usr/share/nginx/html:ro" nginx
