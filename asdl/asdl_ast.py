from pdb import set_trace

from numpy.lib.arraysetops import isin
from .asdl import *

class AbstractSyntaxTree(object):
    def __init__(self, production, realized_fields = None):
        self.production = production
        self.fields = []
        self.parent_field = None
        self.created_time = 0

        if realized_fields:
            assert len(realized_fields) == len(self.production.fields)

            for field in realized_fields:
                self.add_child(field)
        else:
            for field in self.production.fields:
                self.add_child(RealizedField(field))
        
    def add_child(self, realized_field):
        self.fields.append(realized_field)
        realized_field.parent_node = self
    
    def copy(self):
        new_tree = AbstractSyntaxTree(self.production)
        new_tree.created_time = self.created_time
        for i, old_field in enumerate(self.fields):
            new_field = new_tree.fields[i]
            new_field._not_single_cardinality_finished = old_field._not_single_cardinality_finished
            if isinstance(old_field.type, ASDLCompositeType):
                for value in old_field.as_value_list:
                    new_field.add_value(value.copy())
            else:
                for value in old_field.as_value_list:
                    new_field.add_value(value)
        return new_tree
    
class RealizedField(Field):
    def __init__(self, field, value = None, parent = None):
        super(RealizedField, self).__init__(field.name, field.type, field.cardinality)
        self.parent_node = None

        # FIXME: hack, return the field as a property
        self.field = field
        if self.cardinality == 'multiple':
            self.value = []
            if value is not None:
                for child_node in value:
                    self.add_value(child_node)
        else:
            self.value = None
            if value is not None: self.add_value(value)
        self._not_single_cardinality_finished = False
    
    def add_value(self, value):
        if isinstance(value, AbstractSyntaxTree):
            value.parent_field = self
        
        if self.cardinality == 'multiple':
            self.value.append(value)
        else:
            self.value = value
        
    @property
    def as_value_list(self):
        if self.cardinality == 'multiple': return self.value
        elif self.value is not None: return [self.value]
        else: return []
    
    @property
    def finished(self):
        if self.cardinality == 'single':
            if self.value is None: return False
            else: return True
        elif self.cardinality == 'optional' and self.value is not None:
            return True
        else:
            if self._not_single_cardinality_finished: return True
            else: return False
    
    def set_finish(self):
        self._not_single_cardinality_finished = True
    
    def __eq__(self, other):
        if super(RealizedField, self).__eq__(other):
            if type(other) == Field: return True
            if self.value == other.value: return True
            else: return False
        else: return False

