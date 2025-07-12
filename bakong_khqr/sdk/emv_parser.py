class EMVParser:
    def __init__(self, emv_string: str):
        self.raw = emv_string
        self.parsed = self.__parse_tags()

    def __parse_tags(self) -> dict:
        index = 0
        tags = {}
        while index < len(self.raw):
            tag = self.raw[index:index+2]
            length = int(self.raw[index+2:index+4])
            value = self.raw[index+4:index+4+length]
            tags[tag] = value
            index += 4 + length
        return tags

    def get(self, tag: str) -> str:
        return self.parsed.get(tag)
