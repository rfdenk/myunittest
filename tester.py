
import sys
import traceback
import math

__testharness = True

class Testable(object):

    
    class TestError(BaseException):
        pass
        
    def checkTrue(self,f):
        #print('Checking ' + str(f))
        if not f: raise self.TestError()

    def checkFalse(self,f):
        if f: raise self.TestError()
        
    # func is the function to call
    # expected is an exception class
    def checkRaises(self, func, expected):
        didRaise = False
        try:
            func()
        except expected:
            didRaise = True
        finally:
            if not didRaise: 
                #print('Test did not raise exception')
                raise self.TestError()
            
            
class Tester:
    def __init__(self, module='__main__'):

        testables = []
        if(isinstance(module,str)):
            self.testable = __import__(module)
            testables = self.loadTestablesFromModule(self.testable)
            
        #print('Testables = ' + str(testables))
        
        success = True
        errors = []
        testCount = 0
        failCount = 0
        for testable in testables:
            if len(testable[2]) > 0:
                instance = testable[1]()
                try:
                    startFunc = getattr(instance, 'prepareToBeTested')
                    #print('Preparing ' + testable[1].__name__)
                    startFunc()
                    del startFunc
                except:
                    pass        #EAFP
                for test in testable[2]:
                    #print('Executing ' + testable[1].__name__ + '.' + test, end = ' ', flush = True)
                    try:
                        func = getattr(instance, test)
                        try:
                            testCount += 1
                            func()
                            print('.', end='', flush=True)
                        except Testable.TestError as e:
                            failCount += 1
                            t,v,b = sys.exc_info()
                            # skip the methods inside tester.py
                            while b and ('__testharness' in b.tb_frame.f_globals):
                                b = b.tb_next
                            # keep the first remaining frame of the exception, which is the function that
                            # called into Testable; e.g., checkTrue(...)
                            errors.append(traceback.format_exception(t,v,b,1))
                            
                            print('F', end='', flush=True)
                            success = False
                        except BaseException as e:
                            failCount += 1
                            t,v,b = sys.exc_info()
                            # skip the methods inside tester.py
                            while b and ('__testharness' in b.tb_frame.f_globals):
                                b = b.tb_next
                            # keep the first remaining frame of the exception, which is the function that
                            # called into Testable; e.g., checkTrue(...)
                            errors.append(traceback.format_exception(t,v,b,1))
                            
                            print('?', end='', flush=True)
                            success = False
                            
                        del func
                    except:
                        pass
                del instance

        print()
        print()
        
        if success:
            print(' %d Tests passed!' % testCount)
        else:
            print(' %d / %d Tests failed' % (failCount,testCount))
            print()
            digits = int(math.log10(failCount)) + 1
            fmtHeader = '-------------------- failure %0' + str(digits) + 'd --------------------'
            fmtFooter = '-' * (50 + digits)
            fc = 0
            for err in errors:
                fc += 1
                print(fmtHeader % fc)
                print()
                for line in err[1:]:
                    print(line, end='', flush=True)
                print()
                print(fmtFooter)
                print()
        
    # find every class that inherits from Testable (except for 'Testable' itself,
    # and then find all the test methods therein.
    def loadTestablesFromModule(self, module):
        #print('loadTestablesFromModule ' + str(module))
        testNames = []
        for name in dir(module):
            obj = getattr(module,name)
            if isinstance(obj, type) and issubclass(obj, Testable) and (obj.__name__ != 'Testable'):
                testNames.append((module, obj, self.loadTestsFromTestable(obj)))
        return testNames;
       
    # given a class that inherits from Testable, find therein all of the methods that start with 'test'
    def loadTestsFromTestable(self, testableClass):
        #print('getTestNames ' + testableClass.__name__)
        def isTestMethod(name):
            return name.startswith('test') and callable(getattr(testableClass, name))
        testNames = list(filter(isTestMethod, dir(testableClass)))
        return testNames
        
    
            


main = Tester
    