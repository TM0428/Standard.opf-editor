cd "$1"
zip -0 -X "$2" mimetype
zip -r "$2" * -x mimetype