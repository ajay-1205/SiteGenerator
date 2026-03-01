class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return f""
        html_str = ""
        for item in self.props:
            html_str += f" {item}: {self.prop[item]}"
        return html_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value  and
            self.props == other.props
        )


    def to_html(self):
        if self.tag is None:
            return self.value

        props = ""
        if self.props:
            props = " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

        # Handle void elements like img
        if self.tag == "img":
            return f"<{self.tag}{props}>"

        if self.value is None:
            raise ValueError("Leaf node missing value")

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("Error: Tag need to be added")
        elif not children:
             raise ValueError("Error: Children need to be added")

        super().__init__(tag, None, children, props)

    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return False
        return (
            self.tag == other.tag and
            self.children == other.children and
            self.props == other.props
        )


    def to_html(self):
        if not self.tag:
            raise ValueError("Error: Tag need to be added")
        elif not self.children:
            return ValueError("Error: Children is missing")
        
        children = "".join(child.to_html() for child in self.children)
        props = self.props_to_html()

        return f"<{self.tag}{props}>{children}</{self.tag}>"

    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
