file_names = ['1.txt', '2.txt', '3.txt']
sorted_files_by_str_count = dict()
file_contents = dict()

for file_name in file_names:
    with open('dir/' + file_name, "r", encoding="utf-8") as file:
        file_lines = file.readlines()
        sorted_files_by_str_count[file_name] = len(file_lines)
        file_contents[file_name] = ''.join(file_lines)


for file_name, file_str_count in sorted(sorted_files_by_str_count.items(), key=lambda i: i[1], reverse=True):
    print(file_name, file_str_count, file_contents[file_name], sep='\n', end='\n\n')
