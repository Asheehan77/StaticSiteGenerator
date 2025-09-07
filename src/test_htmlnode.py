import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

class TestTextNode(unittest.TestCase):
    def test_props(self):
        tag = "<h>"
        value = "LOL"
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag=tag,value=value,props=props)

    def test_props2(self):
        value = "LOL"
        props = {
            "href": "twitch.tv",
        }
        node = HTMLNode(value=value,props=props)
        
    def test_props3(self):
        tag = "<balls>"
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            "nonsense":"omegalol",
        }
        node = HTMLNode(tag=tag,props=props)
        
    def test_props4(self):
        tag = "<balls>"
        node = HTMLNode(tag=tag)

    
    def test_Leaf(self):
        props = {"href": "https://www.google.com"}
        node = LeafNode("a", "Click me!",props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_Leaf2(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_Leaf3(self):
        node = LeafNode(None,value = "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )



if __name__ == "__main__":
    unittest.main()