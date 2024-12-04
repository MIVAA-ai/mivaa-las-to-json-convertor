from scanners.scanner import Scanner

file_full_path = rf'sample-data/49-005-30258.las'


scanner = Scanner(file_full_path)
normalised_json = scanner.scan()