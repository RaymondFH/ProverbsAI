import re

class BibleLinkGenerator:
    def __init__(self):
        self.bible_websites = {
            'USCCB (NABRE)': 'https://bible.usccb.org/bible/{}',
            'Bible Gateway (KJV)': 'https://www.biblegateway.com/passage/?search={}&version=KJV',
            'Bible Gateway (NIV)': 'https://www.biblegateway.com/passage/?search={}&version=NIV',
            'Biblehub': 'https://biblehub.com/{}',
        }

    def parse_bible_reference(self, text):
        pattern = r'(\d?\s?[A-Za-z]+)\s+(\d+):(\d+)(?:-(\d+))?'
        match = re.search(pattern, text)
        if match:
            book, chapter, verse_start, verse_end = match.groups()
            return {
                'book': book.strip(),
                'chapter': chapter,
                'verse_start': verse_start,
                'verse_end': verse_end
            }
        return None

    def generate_links(self, bible_reference):
        if not bible_reference:
            return {}

        links = {}
        for site_name, url_template in self.bible_websites.items():
            if site_name == 'USCCB (NABRE)':
                book = bible_reference['book'].lower().replace(' ', '')
                verse = f"{bible_reference['chapter']}:{bible_reference['verse_start']}"
                url = url_template.format(f"{book}/{verse}")
            else:
                reference = f"{bible_reference['book']} {bible_reference['chapter']}:{bible_reference['verse_start']}"
                if bible_reference['verse_end']:
                    reference += f"-{bible_reference['verse_end']}"
                url = url_template.format(reference)
            
            links[site_name] = url

        return links

    def process_ai_response(self, ai_response):
        bible_reference = self.parse_bible_reference(ai_response)
        if bible_reference:
            return self.generate_links(bible_reference)
        return {}