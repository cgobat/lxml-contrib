import doctest
import sys
import unittest
from lxml import html

class TestBasicFeatures(unittest.TestCase):
    def test_various_mixins(self):
        base_url = "http://example.org"
        doc = html.fromstring("""
        <root>
            <!-- comment -->
            &entity;
            <el/>
        </root>
        """, base_url=base_url)
        self.assertEqual(doc.getroottree().docinfo.URL, base_url)
        self.assertEqual(len(doc), 2)
        self.assertIsInstance(doc[0], html.HtmlComment)
        self.assertIsInstance(doc[1], html.HtmlElement)
        for child in doc:
            # base_url makes sense on all nodes (kinda) whereas `classes` or
            # `get_rel_links` not really
            self.assertEqual(child.base_url, base_url)

    def test_set_empty_attribute(self):
        e = html.Element('e')
        e.set('a')
        e.set('b', None)
        e.set('c', '')
        self.assertEqual(
            html.tostring(e),
            b'<e a b c=""></e>',
            "Attributes set to `None` should yield empty attributes"
        )
        self.assertEqual(e.get('a'), '', "getting the empty attribute results in an empty string")
        self.assertEqual(e.attrib, {
            'a': '',
            'b': '',
            'c': '',
        })

    def test_element_head_body(self):
        doc = html.fromstring("""
        <HTML>
          <HEAD>
          </HEAD>
          <BODY>
            <p>
          </body>
        </HTML>
        """)

        head = doc.head
        body = doc.body

        self.assertIs(doc.head, head)
        self.assertIs(doc.body, body)
        self.assertIs(doc[0].head, head)
        self.assertIs(doc[0].body, body)
        self.assertIs(doc[1].head, head)
        self.assertIs(doc[1].body, body)
        self.assertIs(doc[1][0].head, head)
        self.assertIs(doc[1][0].body, body)

    def test_element_head_body_empty(self):
        doc = html.fromstring("""
        <HTML>
        </HTML>
        """)
        self.assertIsNone(doc.head)
        self.assertIsNone(doc.body)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([doctest.DocFileSuite('test_basic.txt')])
    suite.addTests([doctest.DocTestSuite(html)])
    suite.addTest(unittest.TestLoader().loadTestsFromModule(sys.modules[__name__]))
    return suite

if __name__ == '__main__':
    unittest.main()
