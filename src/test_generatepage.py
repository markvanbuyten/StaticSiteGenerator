from generate_page import extract_title

def test_extract_title(self):
        # Test 1: Normaal scenario
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

        # Test 2: Titel met extra witruimte en andere tekst eronder
        md = """
#  Title with spaces   

This is a paragraph.
## Subtitle
"""
        # De functie moet de '#' strippen en de extra spaties rondom de titel weghalen
        self.assertEqual(extract_title(md), "Title with spaces")

        # Test 3: Geen H1 header aanwezig (zou een Exception moeten gooien)
        md = "## Only a subtitle"
        with self.assertRaises(Exception):
            extract_title(md)
            
        # Test 4: Geen tekst na de #
        md = "# "
        self.assertEqual(extract_title(md), "")