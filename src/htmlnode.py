class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #A list of HTMLNode objects representing the children of this node
        self.props = props #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        html = ""
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html
    
    def __repr__(self):
        props_str = self.props_to_html()
        children_str =""
        if self.children is not None:
            for child in self.children:
                children_str.join(str(child))
        
        return f"HTMLNode({self.tag}, {self.value}, children: {children_str}, {self.props})"
