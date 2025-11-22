rm -rfd ./bin/dist/css
rm -rfd ./bin/dist/fonts
rm -rfd ./bin/dist/icons

find ./bin/dist -type f -name '*.js.map' -delete
find ./bin/dist -type f -name '*.ico' -delete
find ./bin/dist -type f -name '*.png' -delete