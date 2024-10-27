"""
using:
class ParentState: def **init**(self, parent_id, state): self.parent_id = parent_id self.state = state def **hash**(
self): return hash(self.parent_id) def **eq**(self, other): return (self.parent_id== other.parent_id)

how do i find the ParentState using the parent id
"""