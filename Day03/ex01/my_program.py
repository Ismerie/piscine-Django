from path import Path

def main():

    directory = Path("test_directory")
    directory.mkdir_p()

    file_path = directory / "test_file.txt"
    file_path.touch()


    content = "Bonjour, ceci est un test."
    file_path.write_text(content)

    read_content = file_path.read_text()

    print(read_content)

if __name__ == '__main__':
    main()