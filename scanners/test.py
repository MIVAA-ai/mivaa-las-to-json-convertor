from scanners.scanner import Scanner
from utils.SerialiseJson import JsonSerializable

file_full_path = rf'F:\PyCharmProjects\welllogs-rag\uploads\11_30a-A8_dwl_DWL_WIRE_238588795.las'


scanner = Scanner(file_full_path)
normalised_json = scanner.scan()
print(JsonSerializable.to_json(normalised_json))