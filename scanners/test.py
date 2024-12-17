from scanners.scanner import Scanner
from utils.SerialiseJson import JsonSerializable

file_full_path = rf'F:\PyCharmProjects\welllogs-rag\uploads\11_30a-_9Z_dwl_DWL_WIRE_238615014.las'


scanner = Scanner(file_full_path)
normalised_json = scanner.scan()
# print(normalised_json)
print(JsonSerializable.to_json(normalised_json))