export PATH=/usr/bin/protoc-gen-js:$PATH
protoc -I=. ./src/service.proto --js_out=import_style=commonjs,binary:. --grpc-web_out=import_style=commonjs,mode=grpcwebtext:.