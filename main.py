# from scanners.scanner import Scanner
# import json
# from utils.SerialiseJson import JsonSerializable
#
# file_full_path = rf'sample-data/49-005-31631.las'
#
#
# scanner = Scanner(file_full_path)
# normalised_json = scanner.scan()
# print(JsonSerializable.to_json(normalised_json))
#

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)