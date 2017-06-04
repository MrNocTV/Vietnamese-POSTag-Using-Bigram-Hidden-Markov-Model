import sys 

sys.setrecursionlimit(1000000)
class Node:
    def __init__(self, tag_name, parent=None):
        self.parent = parent
        self.tag_name = tag_name
        self.children = []
        self.text = ''
        self.pos_tag = ''

    def __str__(self):
        if self.text:
            return self.tag_name + ": " + self.pos_tag
        else:
            return self.tag_name

class Parser:
    def __init__(self, parse_string):
        self.parse_string = parse_string 
        self.root = None 
        self.current_node = None 
    
        self.state = FirstTag()
    
    def process(self, remaining_string):
        remaining = self.state.process(remaining_string, self)
        if remaining:
            self.process(remaining)
    
    def start(self):
        self.process(self.parse_string)

class FirstTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find('<')
        i_end_tag = remaining_string.find('>')
        tag_name = remaining_string[i_start_tag+1:i_end_tag]
        root = Node(tag_name)
        parser.root = parser.current_node = root
        parser.state = ChildNode()
        return remaining_string[i_end_tag+1:]
    
class ChildNode:
    def process(self, remaining_string, parser):
        stripped = remaining_string.strip()
        if stripped.startswith("</"):
            parser.state = CloseTag()
        elif stripped.startswith("<"):
            parser.state = OpenTag()
        else:
            parser.state = TextNode()
       
        return stripped

class OpenTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find('<')
        i_end_tag = remaining_string.find('>')
        tag_name = remaining_string[i_start_tag+1:i_end_tag]
        tag_name = tag_name.split()
        pos_tag = ''
        if len(tag_name) > 1:
            pos_tag = tag_name[-1][5:-1]
        tag_name = tag_name[0]
        node = Node(tag_name, parser.current_node)
        # print(pos_tag)
        if pos_tag != '':
            node.pos_tag = pos_tag
        parser.current_node.children.append(node)
        parser.current_node = node 
        parser.state = ChildNode()
        
        return remaining_string[i_end_tag+1:]

class CloseTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        i_end_tag = remaining_string.find(">")
        parser.current_node = parser.current_node.parent
        parser.state = ChildNode()
        
        return remaining_string[i_end_tag+1:].strip()

class TextNode:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        text = remaining_string[:i_start_tag]
        if text:
            parser.current_node.text = text 
        parser.state = ChildNode()
        return remaining_string[i_start_tag:]

if __name__ == '__main__':
    import sys 
    test_file = open(sys.argv[2])
    maxent_output = []
    # read xml contents
    # and get pos tag values 
    with open(sys.argv[1]) as f:
        contents = f.read().strip()
        p = Parser(contents)
        p.start()

        nodes = [p.root]
        tag_seq = ''
        while nodes:
            node = nodes.pop(0)
            if node.pos_tag:
                tag_seq = tag_seq + ' ' +  node.pos_tag
                if len(node.children) == 0 and len(nodes) == 0:
                    if tag_seq:
                        print(tag_seq.strip())
                        maxent_output.append(tag_seq.strip())
            else:
                if tag_seq:
                    print(tag_seq.strip())
                    maxent_output.append(tag_seq.strip())
                tag_seq = ''
            nodes = node.children + nodes 
        
    
    # compare maxent with test 
    total_tag = 0
    correct_tag = 0
    for i, tag_sq in enumerate(maxent_output):
        tag_seq = tag_sq.split()
        tag_test = test_file.readline().strip().split()
        assert len(tag_seq) == len(tag_test)
        total_tag += len(tag_seq)
        for j in range(len(tag_seq)):
            if tag_seq[j] == tag_test[j]:
                correct_tag += 1
    print("Accuracy: {:.2f}".format((correct_tag/total_tag)*100))