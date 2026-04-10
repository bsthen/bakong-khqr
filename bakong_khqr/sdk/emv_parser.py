class EMVParser:
    parsed: dict[str, str]
    
    def __init__(self, emv_string: str):
        self.raw = emv_string
        self.parsed = self.__parse_tags()

    def __parse_tags(self) -> dict:
        index = 0
        tags: dict[str, str] = {}
        while index < len(self.raw):
            try:
                tag = self.raw[index:index+2]
                length_str = self.raw[index+2:index+4]
                if not length_str: break
                length = int(length_str)
                value = self.raw[index+4:index+4+length]
                tags[tag] = value
                index += 4 + length
            except (ValueError, IndexError):
                break
        return tags

    def get(self, tag: str) -> str | None:
        return self.parsed.get(tag)
