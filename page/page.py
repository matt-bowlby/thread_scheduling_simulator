class Page:
    def __init__(self, page_id):
        self.id = page_id                 # unique identifier
        self.loaded = False               # currently in physical memory?
        self.frame_index = None           # which frame (if any)
        self.last_access = -1             # simulation time of last reference
        self.loaded_at = -1               # time it entered memory
        self.access_count = 0             # total accesses so far
        self.modified = False             # was it written to since load?
        self.reference_bit = 0            # for Clock algorithm