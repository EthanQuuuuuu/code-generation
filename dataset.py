class Dataset(object):
  def __init__(self, examples):
    self.examples = examples
  
  @staticmethod
  def from_bin_file(file_path):
    examples = pickle.load(open(file_path, 'rb'), encoding = 'utf-8')
    return Dataset(examples)
 
  
