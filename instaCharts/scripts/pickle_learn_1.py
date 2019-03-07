import pickle
import file

class Thing:
    def __init__(self, s):
        self.s = s
    def __repr__(self):
        return "Thing: %s" % self.s
    def save(self, fileName):
        """Save thing to a file."""
        f = file(fileName,"w")
        pickle.dump(self,f)
        f.close()
    def load(fileName):
        """Return a thing loaded from a file."""
        f = file(fileName,"r")
        obj = pickle.load(f)
        f.close()
        return obj
    # make load a static method
    load = staticmethod(load)

if __name__ == "__main__":
    # code for standalone use
    filename="foo.pickle"
    foo = Thing("fooaaaaaaaaaaaaaa")
    foo.save(filename)
