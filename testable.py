import tester

class A(tester.Testable):
    def __init__(self):
        pass #print('Creating A')
       
    def test1(self):
        #print('Running A.test1')
        self.checkFalse(True)
    
    def test2(self):
        #print('Running A.test2')
        self.checkTrue(True)
    
class B(tester.Testable):

    class BErr(BaseException):
        pass
        
    def __init__(self):
        pass #print('Creating B')
        
        
    def prepareToBeTested(self):
        pass #print('Preparing B')
        
    def test1(self):
        #print('Running B.test1')
        self.checkFalse(False)
    
    def test2(self):
        #print('Running B.test2')
        self.checkTrue(0/0)
    
    def funcB(self):
        #print('In funcB')
        # uncomment the next line to pass test3
        pass #raise self.BErr()
        
    def test3(self):
        #print('In test3')
        self.checkRaises(self.funcB, self.BErr)
        
if __name__ == '__main__':
    tester.main()
    