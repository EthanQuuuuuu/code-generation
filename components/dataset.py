
class Example(object):
    def __init__(self, src_sent, tgt_actions, tgt_code, tgt_ast, idx = 0, meta = None):
        self.src_sent = src_sent
        self.tgt_code = tgt_code
        self.tgt_ast = tgt_ast
        self.tgt_actions = tgt_actions
        self.idx = idx
        self.meta = meta
        