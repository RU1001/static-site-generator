class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        props_str = ""
        for key, val in self.props.items():
            props_str += f' {key}="{val}"'
        
        return props_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    





class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
            
        # Call parent constructor with children=None
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
            # Start with opening tag
        html = f"<{self.tag}"
        
        # Add any properties/attributes
        if self.props:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'
        
        # Close opening tag and add value and closing tag
        html += f">{self.value}</{self.tag}>"
        
        return html
